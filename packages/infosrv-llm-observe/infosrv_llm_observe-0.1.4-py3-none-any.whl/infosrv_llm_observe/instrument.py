from functools import wraps
from .client import get_client
import time
from typing import Callable

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def estimate_cost(tokens: int) -> float:
    return round(tokens * 0.00002, 6)

def instrument(project_id: str = None, user_id: str = "system", session_id: str = "local", model: str = "local-model"):
    """
    Decorator to instrument functions that perform LLM calls.
    - project_id is required on decorator (or caller must call register() and pass default project later).
    The decorated function can return:
      - a string (response body)
      - or a tuple (response_text, tokens, cost)
    """
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start_ts = time.time()
            success = True
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                result = f"__error__:{exc}"
                success = False

            # Normalize
            if isinstance(result, tuple):
                output = result[0]
                tokens = result[1] if len(result) > 1 else estimate_tokens(str(output))
                cost = result[2] if len(result) > 2 else estimate_cost(tokens)
            else:
                output = result
                tokens = estimate_tokens(str(output))
                cost = estimate_cost(tokens)

            # build messages best-effort
            prompt = kwargs.get("prompt") or kwargs.get("user_input") if isinstance(kwargs, dict) else None
            if not prompt and args:
                prompt = args[0] if len(args) > 0 else None
            messages = []
            if prompt is not None:
                messages.append({"role":"user","content": str(prompt)})
            messages.append({"role":"assistant","content": str(output)})

            # send trace non-blocking style (we call but ignore exceptions)
            try:
                client = get_client()
                if project_id is None:
                    raise RuntimeError("instrument decorator requires project_id argument")
                client.send_trace(project_id=project_id, user_id=user_id, session_id=session_id, messages=messages, model=model, tokens=tokens, cost=cost)
            except Exception:
                pass

            if success:
                return result
            raise RuntimeError("Instrumented function failed") from None

        return wrapper
    return decorator
