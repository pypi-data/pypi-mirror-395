# tasks/persistence/db_adapter.py
import logging
import traceback
from datetime import datetime, UTC

from .port import BasePersistence
from ..core.events import TaskLifecycleEvent
from ..core.status import TaskStatus
from ..persistence.repository.context import save_context
from ..persistence.repository.report import (
    init_report_from_context,
    save_report,
    update_report,
)

log = logging.getLogger("DBPersistence")


class DBPersistence(BasePersistence):
    """
    Idempotent(ish) persistence adapter.
    - RUNNING: ensure context saved, create initial report row
    - FINAL (SUCCESS/FAILED/CANCELLED/SKIPPED/DEAD/TIMEOUT): update report
    - SKIPPED: write a minimal skipped report if none exists
    """

    def on_created(self, e: TaskLifecycleEvent) -> None:
        """Persist context as soon as a task is created/submitted."""
        try:
            save_context(e.context)
        except Exception:
            log.exception("persist created failed (non-fatal)")

        try:
            report = init_report_from_context(e.context)
            update_report(report)
        except Exception:
            log.exception("persist report failed (non-fatal)")


    def on_running(self, e: TaskLifecycleEvent) -> None:
        ctx = e.context
        try:
            # In case QUEUED wasn't persisted at submit time
            save_context(ctx)
        except Exception:
            log.exception("save_context failed (non-fatal)")

        try:
            report = init_report_from_context(ctx)
            report.worker_id = getattr(ctx, "worker_id", None)
            # If you want a "started_at" timestamp on report, set it here.
            save_report(report)  # should be safe if you do get-or-create in repo
        except Exception:
            log.exception("save_report (init) failed (non-fatal)")

    def on_failed(self, e: TaskLifecycleEvent) -> None:
        """Persist a FAILED outcome with error details and logs."""
        ctx = e.context
        try:
            report = init_report_from_context(ctx)
            report.status = TaskStatus.FAILED
            report.end_time = datetime.now(UTC)
            report.duration = (report.end_time - report.start_time).total_seconds()
            report.worker_id = getattr(ctx, "worker_id", None)

            # Logs collected by the runner thread handler, if any
            log_handler = getattr(ctx, "thread_handler", None)
            if log_handler:
                try:
                    report.logs = log_handler.get_stream_value()
                except Exception:
                    pass

            # Merge error details from event.meta and ctx.extra_context
            meta = e.meta or {}

            # Normalize exception traceback
            tb_val = meta.get('exception')
            if tb_val is None:
                tracebacks = None
            elif isinstance(tb_val, Exception):
                tracebacks = traceback.format_exception(type(tb_val), tb_val, tb_val.__traceback__)
            elif isinstance(tb_val, str):
                tracebacks = [tb_val]
            elif isinstance(tb_val, (list, tuple)):
                tracebacks = [str(t) for t in tb_val]
            else:
                tracebacks = [str(tb_val)]
            report.tracebacks = tracebacks

            reason = meta.get("reason")
            report.error = {k: v for k, v in {
                "message": str(tb_val),
                "type": type(tb_val).__name__,
                "reason": reason,
            }.items() if v is not None}

            update_report(report)
        except Exception:
            log.exception("persist failed update failed (non-fatal)")

    def on_final(self, e: TaskLifecycleEvent) -> None:
        ctx = e.context
        try:
            # Build a report snapshot and push update
            report = init_report_from_context(ctx)
            report.end_time = datetime.now(UTC)
            report.duration = (report.end_time - report.start_time).total_seconds()
            report.status = e.status
            report.result = e.meta.get('result', None)
            # pull logs from the runner-attached handler if present
            log_handler = getattr(ctx, "thread_handler", None)
            if log_handler:
                try:
                    report.logs = log_handler.get_stream_value()
                except Exception:
                    pass
            update_report(report)
        except Exception:
            log.exception("update_report failed (non-fatal)")

    def on_skipped(self, e: TaskLifecycleEvent) -> None:
        ctx = e.context
        try:
            report = init_report_from_context(ctx)
            report.status = TaskStatus.SKIPPED
            report.end_time = datetime.now(UTC)
            report.duration = (report.end_time - report.start_time).total_seconds()
            report.logs = (report.logs or "") + "⛔ Task skipped due to concurrency lock."
            update_report(report)
        except Exception:
            log.exception("persist skipped failed (non-fatal)")
