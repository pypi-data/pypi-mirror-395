# src/jules_cli/core/api.py
import os
import time
import json
from typing import Optional, Dict, Any, List
import requests
from ..utils.logging import logger
from ..utils.exceptions import JulesAPIError
from ..utils.config import config

# Configuration
BASE = os.getenv("JULES_API_URL", "https://jules.googleapis.com/v1alpha")
POLL_INTERVAL = 5
POLL_TIMEOUT = config.get_nested("core", "api_timeout", 120)

def _http_request(method: str, path: str, json_data: Optional[dict] = None, params: Optional[dict] = None, timeout=None):
    if timeout is None:
        timeout = config.get_nested("core", "api_timeout", 60)

    jules_key = os.getenv("JULES_API_KEY") or config.get_nested("core", "jules_api_key")
    if not jules_key:
        raise JulesAPIError("JULES_API_KEY is not set in environment or config. Please set the JULES_API_KEY environment variable or run `jules init`.")
    headers = {"X-Goog-Api-Key": jules_key, "Content-Type": "application/json"}

    url = f"{BASE}{path}"
    try:
        resp = requests.request(method, url, headers=headers, json=json_data, params=params, timeout=timeout)
    except Exception as e:
        raise JulesAPIError(f"HTTP request failed: {e}")
    if resp.status_code == 401:
        raise JulesAPIError(f"401 UNAUTHENTICATED from Jules API. Check API key.\nBody: {resp.text}")
    if resp.status_code >= 400:
        raise JulesAPIError(f"Jules API returned {resp.status_code}:\n{resp.text}")
    try:
        return resp.json()
    except ValueError:
        raise JulesAPIError(f"Invalid JSON response: {resp.text[:2000]}")

def list_sources() -> List[dict]:
    return _http_request("GET", "/sources").get("sources", [])

def pick_source_for_repo(repo_name: str) -> Optional[dict]:
    # Try to parse repo_name as 'owner/repo'
    parsed_owner = None
    parsed_repo_short = None
    if "/" in repo_name:
        parts = repo_name.split("/", 1)
        parsed_owner = parts[0]
        parsed_repo_short = parts[1]
    
    all_sources = list_sources()

    # Prioritize matching by owner/repo or full source name
    for s in all_sources:
        gr = s.get("githubRepo") or {}
        source_owner = gr.get("owner")
        source_repo_short = gr.get("repo")
        source_name = s.get("name")

        if parsed_owner and parsed_repo_short:
            # Match against parsed owner/repo
            if source_owner == parsed_owner and source_repo_short == parsed_repo_short:
                return s
        
        # Fallback to matching against full source name if provided repo_name is a full source name
        if source_name == repo_name:
            return s

    # Fallback to matching by just repo_short if full owner/repo or source name wasn't found
    target_short = parsed_repo_short if parsed_repo_short else repo_name
    for s in all_sources:
        gr = s.get("githubRepo") or {}
        source_repo_short = gr.get("repo")
        if source_repo_short == target_short:
            return s

    # Finally, try a substring match as a last resort (original logic)
    for s in all_sources:
        if repo_name in (s.get("name") or ""):
            return s

    return None

def create_session(prompt: str, source_name: str, starting_branch="main", title="Jules CLI session", automation_mode=None, branch_name: Optional[str] = None) -> dict:
    payload = {
        "prompt": prompt,
        "sourceContext": {"source": source_name, "githubRepoContext": {"startingBranch": starting_branch}},
        "title": title
    }

    if automation_mode:
        payload["automationMode"] = automation_mode
    return _http_request("POST", "/sessions", json_data=payload)

def list_sessions(page_size=20):
    return _http_request("GET", "/sessions", params={"pageSize": page_size})

def get_session(session_id: str):
    return _http_request("GET", f"/sessions/{session_id}")

def list_activities(session_id: str, page_size=50):
    return _http_request("GET", f"/sessions/{session_id}/activities", params={"pageSize": page_size})

def send_message(session_id: str, prompt: str):
    return _http_request("POST", f"/sessions/{session_id}:sendMessage", json_data={"prompt": prompt})

def poll_for_result(session_id: str, timeout=POLL_TIMEOUT):
    t0 = time.time()
    logger.info(f"Polling session {session_id} for up to {timeout}s...")
    # Add a small initial delay to allow session propagation
    time.sleep(2)
    last_agent_message = None # To store any agent messages found
    while True:
        # 1. Check Activities
        try:
            activities = list_activities(session_id).get("activities", [])
            for act in reversed(activities): # newest-first
                # Check for agent messages within activities
                agent_messaged = act.get("agentMessaged")
                if agent_messaged and agent_messaged.get("agentMessage"):
                    last_agent_message = agent_messaged["agentMessage"]
                    # If an agent message is found, and no other artifacts or plans, return it immediately
                    if not act.get("artifacts") and not act.get("planGenerated"):
                        return {"type": "message", "message": last_agent_message, "session": get_session(session_id)}

                # Check for planGenerated activities
                plan_generated = act.get("planGenerated")
                if plan_generated and plan_generated.get("plan"):
                    return {"type": "plan", "plan": plan_generated["plan"], "activity": act, "session": get_session(session_id)}
                
                # Check for artifacts (Patches, PRs)
                if act.get("artifacts"):
                    for art in act["artifacts"]:
                        cs = art.get("changeSet")
                        if cs:
                            gp = cs.get("gitPatch") or {}
                            patch = gp.get("unidiffPatch")
                            if patch:
                                return {"type": "patch", "patch": patch, "activity": act}
                        
                        pr = art.get("pullRequest")
                        if pr:
                            return {"type": "pr", "pr": pr, "activity": act}

        except JulesAPIError as e:
            # Swallow 404s during polling (eventual consistency)
            if "404" in str(e) or "NOT_FOUND" in str(e):
                logger.debug(f"Session {session_id} activities not visible yet (404). Retrying...")
            else:
                raise e

        # 2. Check Session Outputs and State (after checking activities)
        sess = None
        try:
            sess = get_session(session_id)
            if sess.get("outputs"):
                for out in sess["outputs"]:
                    if out.get("pullRequest"):
                        return {"type": "pr", "pr": out["pullRequest"], "session": sess}
                    # Also check for agent messages in outputs if they can appear there directly
                    if out.get("agentMessaged") and out["agentMessaged"].get("agentMessage"):
                        return {"type": "message", "message": out["agentMessaged"]["agentMessage"], "session": sess}
        except JulesAPIError as e:
            if "404" in str(e) or "NOT_FOUND" in str(e):
                pass # Session might not be fully propagated yet, continue polling
            else:
                raise e

        # If session reached a terminal state (COMPLETED, FAILED, CANCELLED)
        if sess and sess.get("state") in ["COMPLETED", "FAILED", "CANCELLED"]:
            if last_agent_message: # If we have a message from activities, return it as the final result
                return {"type": "message", "message": last_agent_message, "session": sess}
            else: # Otherwise, return the session status
                return {"type": "session_status", "status": sess["state"], "session": sess}
        
        # If in PLANNING state and no definitive output yet, allow to proceed until timeout.
        if sess and sess.get("state") == "PLANNING":
            # If a message was found, but not returned immediately (because of other artifacts), and we're still in PLANNING
            if last_agent_message:
                return {"type": "message", "message": last_agent_message, "session": sess}
            pass

        # Timeout Check
        if time.time() - t0 > timeout:
            raise JulesAPIError("Timed out waiting for Jules outputs.")
        time.sleep(POLL_INTERVAL)

def approve_plan(session_id: str):
    """
    Approves the plan for the given session.
    """
    logger.info(f"Approving plan for session {session_id}...")
    return _http_request("POST", f"/sessions/{session_id}:approvePlan")
