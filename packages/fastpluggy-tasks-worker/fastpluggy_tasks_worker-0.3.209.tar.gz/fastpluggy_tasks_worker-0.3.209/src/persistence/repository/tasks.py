from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..models.report import TaskReportDB
from ...persistence.models.context import TaskContextDB


from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased

from ...core.status import task_status_badge_class

def get_task_context_and_report(
    db,
    task_id: str | None = None,
    limit: int = 20,
    filter_criteria=None,
):
    """
    Returns a list of tuples: (TaskContextDB, TaskReportDB | None)
    - One report per task_id, so a simple LEFT JOIN is enough.
    - LIMIT applies to contexts (ordered by id desc).
    - If time filters are used, contexts with no report are still included.
    """

    # 1) Select contexts first (so LIMIT applies to contexts)
    base_ctx_q = db.query(TaskContextDB)
    if task_id:
        base_ctx_q = base_ctx_q.filter(TaskContextDB.task_id == task_id)

    ctx_subquery = base_ctx_q.order_by(desc(TaskContextDB.id)).limit(limit).subquery()
    TaskContext = aliased(TaskContextDB, ctx_subquery)

    # 2) Left join the single report per task
    query = (
        db.query(TaskContext, TaskReportDB)
        .outerjoin(TaskReportDB, TaskReportDB.task_id == TaskContext.task_id)
    )

    # 3) Optional filters (only when not targeting one specific task)
    if not task_id and filter_criteria:
        # Task name filter on contexts
        if getattr(filter_criteria, "task_name", None):
            query = query.filter(
                TaskContext.task_name.ilike(f"%{filter_criteria.task_name}%")
            )

        # Time filters on TaskReportDB
        start_time = getattr(filter_criteria, "start_time", None)
        end_time = getattr(filter_criteria, "end_time", None)

        if start_time and end_time:
            query = query.filter(
                or_(
                    TaskReportDB.start_time.is_(None),
                    and_(
                        TaskReportDB.start_time >= start_time,
                        TaskReportDB.start_time <= end_time,
                    ),
                )
            )
        elif start_time:
            query = query.filter(
                or_(
                    TaskReportDB.start_time.is_(None),
                    TaskReportDB.start_time >= start_time,
                )
            )
        elif end_time:
            query = query.filter(
                or_(
                    TaskReportDB.start_time.is_(None),
                    TaskReportDB.start_time <= end_time,
                )
            )

    # 4) Execute and return
    return query.all()


def get_task_context_reports_and_format(db: Session, task_id: str = None, limit: int = 20, filter_criteria=None):
    rows = get_task_context_and_report(db=db, task_id=task_id, limit=limit, filter_criteria=filter_criteria)

    return [
        {
            "task_id": context.task_id,
            "task_name": context.task_name,
            "function": context.func_name,
            "args": context.args,
            "kwargs": context.kwargs,
            "notifier_config": context.notifier_config,
            "result": report.result if report else None,
            "logs": report.logs if report else None,
            "duration": report.duration if report else None,
            "error": report.error if report else None,
            "tracebacks": report.tracebacks if report else None,
            "attempts": report.attempts if report else None,
            "success": report.success if report else None,
            "status": report.status if report else None,
            "status_css_class": task_status_badge_class(report.status) if report and report.status else task_status_badge_class('unknown'),
            "start_time": report.start_time.isoformat() if report and report.start_time else None,
            "end_time": report.end_time.isoformat() if report and report.end_time else None,
        }
        for context, report in rows
    ]

