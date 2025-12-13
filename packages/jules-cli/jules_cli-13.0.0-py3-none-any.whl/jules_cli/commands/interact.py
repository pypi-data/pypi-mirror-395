# src/jules_cli/commands/interact.py

import typer
import time
from typing import Optional
from ..core.api import create_session, send_message, poll_for_result, pick_source_for_repo, list_sources
from ..utils.logging import logger
from ..state import _state
from ..utils.exceptions import JulesAPIError
from ..utils.config import config # Import the config object

def cmd_interact(prompt: str):
    """
    Start an interactive session with Jules to refine goals before planning.
    """
    logger.info("Starting interactive session with Jules...")
    
    session_id = None # Initialize session_id to None
    try:
        repo_dir_name = config.get_nested("core", "default_repo")
        if not repo_dir_name:
            logger.error("No default repository configured. Please set it using 'jules config set default_repo <owner/repo>'.")
            return {"status": "error", "message": "No default repository configured."}

        source_obj = pick_source_for_repo(repo_dir_name)
        if not source_obj:
            available = [s.get("name") for s in list_sources()]
            logger.error(f"No Jules API source found for repository '{repo_dir_name}'. Available sources: {available}")
            return {"status": "error", "message": f"No API source found for '{repo_dir_name}'."}
            
        source_name = source_obj.get("name")
        
        session = create_session(prompt=prompt, source_name=source_name)
        session_id = session.get("name").split("/")[-1]
        _state["current_session"] = session
        _state["session_id"] = session_id
        
        logger.info(f"Session '{session_id}' created for source '{source_name}'. Waiting for Jules's response...")
        
        while True:
            # Poll for Jules's response
            try:
                result = poll_for_result(session_id)
            except JulesAPIError as e:
                logger.error(f"Error polling for result: {e}")
                break
            
            if result["type"] == "message":
                message = result["message"]
                logger.info(f"\nJules: {message}")
            elif result["type"] == "plan":
                plan = result["plan"]
                logger.info(f"\nJules has proposed a plan:\n{plan}\n")
                logger.info("You can now `jules approve` or `jules reject` this plan.")
                break # Exit interaction mode, user takes action via separate command
            elif result["type"] == "patch":
                logger.info("\nJules generated a patch. Use `jules apply` to apply it.")
                break
            elif result["type"] == "pr":
                logger.info("\nJules created a pull request.")
                break
            elif result["type"] == "session_status":
                status = result["status"]
                logger.info(f"\nSession {session_id} reached terminal state: {status}")
                if status == "FAILED":
                    logger.error("Session failed. Please check logs or try again.")
                break
            
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                logger.info("Exiting interactive session.")
                break
            
            # Send user input to Jules
            send_message(session_id, user_input)
            logger.info("Message sent. Waiting for Jules's response...")
            time.sleep(2) # Small delay before next poll
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        
    return {"status": "success", "session_id": session_id}
