import json
import logging
from typing import Optional, Callable

from ..models.scheduled import ScheduledTaskDB


def _to_qualified_name(value: Callable | str) -> str:
    """Return function identifier as 'module:qualname'.
    - If callable: build from __module__ and __qualname__.
    - If string and already contains ':', return as-is.
    - If string with a dot, assume 'module.qualname' and convert to 'module:qualname'.
    - If bare string (no ':' or '.'), try to resolve from the task registry and expand.
    - Otherwise return the original string (best-effort backward compatibility).
    """
    if callable(value):
        return f"{value.__module__}:{value.__qualname__}"
    if isinstance(value, str):
        if ":" in value:
            return value
        if "." in value:
            module, qual = value.split(".", 1)
            return f"{module}:{qual}"
        # Try resolving bare name via registry
        try:
            from ...registry.registry import task_registry  # type: ignore
            func = task_registry.get(value)
            if func is not None:
                return f"{func.__module__}:{func.__qualname__}"
        except Exception:
            pass
        return value
    return str(value)


def ensure_scheduled_task_exists(
        db,
        function: Callable | str,
        task_name: Optional[str] = None,
        cron: Optional[str] = None,
        interval: Optional[int] = None,
        kwargs: Optional[dict] = None,
        allow_concurrent: bool = False,
        max_retries: int = 0,
        retry_delay: int = 0,
        enabled: bool = False,
        topic: Optional[str] = None,
        origin: Optional[str] = None,
):
    """
    Ensure a ScheduledTaskDB entry exists for the given function and schedule.
    Uniqueness is based on (function, cron) or (function, interval) rather than the task name,
    to avoid duplicates when different names point to the same scheduled task.

    - `function` can be a callable or a string; it is normalized to 'module:qualname'.
    - `task_name` is only a display label; it does not enforce uniqueness anymore.
    - If an entry already exists, update the `enabled` flag if it differs.
    """
    # Normalize function identifier for uniqueness
    function_name = _to_qualified_name(function)

    # Default task_name to a readable value if not provided
    if task_name is None:
        task_name = function.__name__ if callable(function) else str(function)

    # Build a uniqueness filter using function + schedule (cron or interval)
    query = db.query(ScheduledTaskDB).filter_by(function=function_name)
    if cron is not None:
        query = query.filter_by(cron=cron)
    if interval is not None:
        query = query.filter_by(interval=interval)
    if cron is None and interval is None:
        # Fallback: match records with no explicit schedule stored
        query = query.filter_by(cron=None, interval=None)

    existing = query.first()

    if not existing:
        scheduled = ScheduledTaskDB(
            name=task_name,
            cron=cron,
            interval=interval,
            function=function_name,
            kwargs=json.dumps(kwargs or {}),
            # notify_on removed; capability deprecated
            # max_retries=max_retries,
            # retry_delay=retry_delay,
            allow_concurrent=allow_concurrent,
            enabled=enabled,
            topic=topic,
            origin=origin,
        )
        db.add(scheduled)
        db.commit()
        logging.info(
            f"[SCHEDULER] Created ScheduledTaskDB entry for function='{function_name}' "
            f"cron='{cron}' interval='{interval}' as name='{task_name}'"
        )
    else:
        if existing.enabled != enabled:
            existing.enabled = enabled
            db.commit()
            logging.info(
                f"[SCHEDULER] Updated 'enabled' for function='{function_name}' "
                f"cron='{cron}' interval='{interval}' to {enabled} (name='{task_name}')"
            )
        else:
            logging.info(
                f"[SCHEDULER] ScheduledTaskDB already exists for function='{function_name}' "
                f"cron='{cron}' interval='{interval}' (name='{task_name}')"
            )