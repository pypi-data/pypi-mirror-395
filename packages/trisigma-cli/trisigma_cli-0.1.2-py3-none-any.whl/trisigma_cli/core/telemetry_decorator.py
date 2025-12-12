import asyncio
import functools
import time
from typing import Any, Callable, Optional

import typer

from .telemetry_global import track_event


def track_command(
    event_type: str,
    action: Optional[str] = None,
):
    def decorator(func: Callable) -> Callable:
        command_action = action or func.__name__

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()

                try:
                    result = await func(*args, **kwargs)
                    duration_ms = int((time.time() - start_time) * 1000)
                    track_event(
                        event_type=event_type,
                        action=command_action,
                        result="success",
                        duration_ms=duration_ms,
                    )
                    return result
                except Exception as e:
                    duration_ms = int((time.time() - start_time) * 1000)

                    if isinstance(e, typer.Exit):
                        if e.exit_code == 0:
                            track_event(
                                event_type=event_type,
                                action=command_action,
                                result="success",
                                duration_ms=duration_ms,
                            )
                        else:
                            track_event(
                                event_type=event_type,
                                action=command_action,
                                result="error",
                                duration_ms=duration_ms,
                                error_type=f"ExitCode{e.exit_code}",
                                error_message=f"Command exited with code {e.exit_code}",
                            )
                    else:
                        track_event(
                            event_type=event_type,
                            action=command_action,
                            result="error",
                            duration_ms=duration_ms,
                            error_type=type(e).__name__,
                            error_message=str(e)[:500],
                        )
                    raise

            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    duration_ms = int((time.time() - start_time) * 1000)
                    track_event(
                        event_type=event_type,
                        action=command_action,
                        result="success",
                        duration_ms=duration_ms,
                    )
                    return result
                except Exception as e:
                    duration_ms = int((time.time() - start_time) * 1000)

                    if isinstance(e, typer.Exit):
                        if e.exit_code == 0:
                            track_event(
                                event_type=event_type,
                                action=command_action,
                                result="success",
                                duration_ms=duration_ms,
                            )
                        else:
                            track_event(
                                event_type=event_type,
                                action=command_action,
                                result="error",
                                duration_ms=duration_ms,
                                error_type=f"ExitCode{e.exit_code}",
                                error_message=f"Command exited with code {e.exit_code}",
                            )
                    else:
                        track_event(
                            event_type=event_type,
                            action=command_action,
                            result="error",
                            duration_ms=duration_ms,
                            error_type=type(e).__name__,
                            error_message=str(e)[:500],
                        )
                    raise

            return sync_wrapper

    return decorator
