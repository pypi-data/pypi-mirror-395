import inspect
import os
from functools import wraps
from ..state import _state
from ..db import add_history_record
from ..utils.output import print_json

def with_output_handling(func):
    """
    Decorator to handle JSON output for Typer commands.
    It expects the command function to return a result dict.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if _state.get("json_output"):
            print_json(result, pretty=_state.get("pretty"))
        return result
    return wrapper

def record_history(prompt_arg_name: str = None, status: str = "success", prompt_template: str = None):
    """
    Decorator to handle history recording.
    Uses inspect.signature to bind arguments correctly, handling both positional and keyword arguments.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Run the command first
            result = func(*args, **kwargs)

            # Get session ID
            sess = _state.get("current_session")
            session_id = sess.get("id") if sess else _state.get("session_id")
            if not session_id:
                session_id = os.urandom(8).hex()
                _state["session_id"] = session_id

            # Bind arguments to parameter names
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            all_args = bound_args.arguments

            # Determine prompt
            prompt = ""
            if prompt_arg_name and prompt_arg_name in all_args:
                prompt = all_args[prompt_arg_name]
            elif prompt_template:
                # Use all_args for formatting, so it works with positional args too
                try:
                    prompt = prompt_template.format(**all_args)
                except KeyError:
                    # Fallback if template keys are missing
                    prompt = prompt_template

            # Clean up prompt if it's None
            if prompt is None:
                prompt = ""

            add_history_record(session_id=session_id, prompt=prompt, status=status)

            return result
        return wrapper
    return decorator
