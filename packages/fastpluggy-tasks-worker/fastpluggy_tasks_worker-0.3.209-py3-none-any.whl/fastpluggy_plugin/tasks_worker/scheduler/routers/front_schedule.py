import json

from fastapi import Request, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.menu.decorator import menu_entry
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.widgets import AutoLinkWidget
from fastpluggy.core.widgets.categories.input.button_list import ButtonListWidget
from fastpluggy.core.widgets.categories.display.custom import CustomTemplateWidget
from ...config import TasksRunnerSettings
from ...persistence.models.scheduled import ScheduledTaskDB
from ...routers.schema import CreateScheduledTaskRequest, UpdateScheduledTaskRequest
from ...widgets.task_form import TaskFormView
from ...persistence.repository.scheduled import _to_qualified_name as normalize_function

front_schedule_task_router = APIRouter(
    prefix='/scheduled_task',
    tags=["task_router"],
)


@menu_entry(label="Scheduled List", icon='fa-solid fa-clock', )
@front_schedule_task_router.get("/", name="list_scheduled_tasks")
def list_scheduled_tasks(
    request: Request, 
    view_builder=Depends(get_view_builder), 
    db: Session = Depends(get_db),
    search: str = None,
    origin: str = None,
    status: str = None,
    late_only: bool = False
):
    buttons = []
    settings = TasksRunnerSettings()
    if settings.allow_create_schedule_task:
        buttons.append(AutoLinkWidget(label="Create a Scheduled Task", route_name='create_scheduled_task', ))
    if settings.scheduler_enabled and settings.store_task_db:
            buttons.append(AutoLinkWidget(label='Scheduled Task Monitoring', route_name='scheduled_task_monitoring', icon="ti ti-activity"))
    
    # Build query with filters
    query = db.query(ScheduledTaskDB)
    
    # Filter by search term (name or function)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (ScheduledTaskDB.name.ilike(search_term)) | 
            (ScheduledTaskDB.function.ilike(search_term))
        )
    
    # Filter by origin
    if origin and origin != "all":
        query = query.filter(ScheduledTaskDB.origin == origin)
    
    # Filter by enabled/disabled status
    if status == "enabled":
        query = query.filter(ScheduledTaskDB.enabled == True)
    elif status == "disabled":
        query = query.filter(ScheduledTaskDB.enabled == False)
    
    # Fetch tasks
    tasks = query.all()
    
    # Filter by late status (done in Python since is_late is a property)
    if late_only:
        tasks = [task for task in tasks if task.is_late and task.enabled]
    
    # Get unique origins for filter dropdown
    all_origins = db.query(ScheduledTaskDB.origin).distinct().all()
    origins = [o[0] for o in all_origins if o[0]]
    
    items = [
        ButtonListWidget(
            buttons=buttons
        ),
        CustomTemplateWidget(
            template_name="tasks_worker/scheduled_tasks_list.html.j2",
            context={
                "request": request,
                "tasks": tasks,
                "url_task_details": str(request.url_for("task_details", task_id="TASK_ID_REPLACE")),
                "url_edit_task": str(request.url_for("edit_scheduled_task", task_id="TASK_ID_REPLACE")),
                "url_toggle_task": str(request.url_for("toggle_scheduled_task", task_id="TASK_ID_REPLACE")),
                "origins": origins,
                "current_search": search or "",
                "current_origin": origin or "all",
                "current_status": status or "all",
                "current_late_only": late_only,
            }
        )
    ]

    return view_builder.generate(
        request,
        title="List of scheduled tasks",
        widgets=items
    )


@front_schedule_task_router.get("/create", name="create_scheduled_task")
def create_scheduled_task(
        request: Request,
        view_builder=Depends(get_view_builder)
):
    view = TaskFormView(
        title="New Scheduled Task",
        submit_url=str(request.url_for("create_scheduled_task_post")),
        url_after_submit=str(request.url_for("list_scheduled_tasks")),
        mode="schedule_task",
    )
    return view_builder.generate(request, widgets=[view])


@front_schedule_task_router.post("/create", name="create_scheduled_task_post")
def create_scheduled_task_post(
        request: Request,
        payload: CreateScheduledTaskRequest,
        method: str = 'web',
        db: Session = Depends(get_db)
):

    if payload.name is None:
        payload.name = payload.function

    normalized_function = normalize_function(payload.function)

    task = ScheduledTaskDB(
        name=payload.name,
        function=normalized_function,
        cron=payload.cron,
        interval=payload.interval,
        kwargs=json.dumps(payload.kwargs),
        # notify_on disabled for now
        # notify_on=json.dumps(payload.notify_on),
        enabled=True,
        topic=payload.topic,
        origin="webui_create",
    )
    db.add(task)
    db.commit()
    mesg = FlashMessage.add(request=request, message=f"Scheduled Task {payload.name} created !")

    if method == "web":
        return redirect_to_previous(request)
    else:
        return JSONResponse(content=mesg.to_dict())


@front_schedule_task_router.get("/edit/{task_id}", name="edit_scheduled_task")
def edit_scheduled_task(
        request: Request,
        task_id: int,
        view_builder=Depends(get_view_builder),
        db: Session = Depends(get_db)
):
    # Get the scheduled task from database
    task = db.query(ScheduledTaskDB).filter(ScheduledTaskDB.id == task_id).first()
    if not task:
        FlashMessage.add(request=request, message=f"Scheduled Task with ID {task_id} not found!", category="error")
        return redirect_to_previous(request)

    # Parse kwargs from JSON string
    kwargs_dict = {}
    if task.kwargs:
        try:
            kwargs_dict = json.loads(task.kwargs)
        except:
            kwargs_dict = {}

    # Prepare task data for the template
    task_data = {
        "id": task.id,
        "name": task.name,
        "function": task.function,
        "cron": task.cron,
        "interval": task.interval,
        "enabled": task.enabled,
        "allow_concurrent": task.allow_concurrent,
        "topic": task.topic,
        "origin": task.origin,
        "kwargs": json.dumps(kwargs_dict, indent=2),
        "last_attempt": task.last_attempt.strftime('%Y-%m-%d %H:%M:%S') if task.last_attempt else None,
        "last_task_id": task.last_task_id,
        "last_status": task.last_status
    }

    # Create custom template widget
    widget = CustomTemplateWidget(
        template_name="tasks_worker/scheduled_task_edit.html.j2",
        context={
            "task": task_data,
            "submit_url": str(request.url_for("edit_scheduled_task_post", task_id=task_id)),
            "cancel_url": str(request.url_for("list_scheduled_tasks")),
            "url_list_available_tasks": str(request.url_for("list_available_tasks"))
        }
    )

    return view_builder.generate(
        request,
        title=f"Edit Scheduled Task: {task.name}",
        widgets=[widget]
    )


@front_schedule_task_router.post("/edit/{task_id}", name="edit_scheduled_task_post")
def edit_scheduled_task_post(
        request: Request,
        task_id: int,
        payload: UpdateScheduledTaskRequest,
        method: str = 'web',
        db: Session = Depends(get_db)
):
    # Get the scheduled task from database
    task = db.query(ScheduledTaskDB).filter(ScheduledTaskDB.id == task_id).first()
    if not task:
        mesg = FlashMessage.add(request=request, message=f"Scheduled Task with ID {task_id} not found!", category="error")
        if method == "web":
            return redirect_to_previous(request)
        else:
            return JSONResponse(content=mesg.to_dict(), status_code=404)

    # Update only provided fields
    if payload.name is not None:
        task.name = payload.name
    if payload.function is not None:
        task.function = normalize_function(payload.function)
    if payload.cron is not None:
        task.cron = payload.cron
    if payload.interval is not None:
        task.interval = payload.interval
    if payload.kwargs is not None:
        task.kwargs = json.dumps(payload.kwargs)
    if payload.enabled is not None:
        task.enabled = payload.enabled
    if payload.allow_concurrent is not None:
        task.allow_concurrent = payload.allow_concurrent
    if payload.topic is not None:
        task.topic = payload.topic
    task.origin = 'webui_edit'

    db.commit()
    mesg = FlashMessage.add(request=request, message=f"Scheduled Task {task.name} updated successfully!")

    if method == "web":
        return redirect_to_previous(request)
    else:
        return JSONResponse(content=mesg.to_dict())


@front_schedule_task_router.get("/stats", name="scheduled_tasks_stats")
def get_scheduled_tasks_stats(db: Session = Depends(get_db)):
    """
    Get statistics about scheduled tasks
    """
    total_count = db.query(ScheduledTaskDB).count()
    enabled_count = db.query(ScheduledTaskDB).filter(ScheduledTaskDB.enabled == True).count()
    disabled_count = total_count - enabled_count

    return JSONResponse(content={
        "total": total_count,
        "enabled": enabled_count,
        "disabled": disabled_count
    })


@front_schedule_task_router.post("/toggle/{task_id}", name="toggle_scheduled_task")
def toggle_scheduled_task(
        request: Request,
        task_id: int,
        db: Session = Depends(get_db)
):
    """
    Toggle the enabled status of a scheduled task
    """
    task = db.query(ScheduledTaskDB).filter(ScheduledTaskDB.id == task_id).first()
    if not task:
        return JSONResponse(
            content={"success": False, "message": f"Task with ID {task_id} not found"},
            status_code=404
        )
    
    # Toggle the enabled status
    task.enabled = not task.enabled
    db.commit()
    
    status_text = "enabled" if task.enabled else "disabled"
    FlashMessage.add(request=request, message=f"Task '{task.name}' has been {status_text}")
    
    return JSONResponse(content={
        "success": True,
        "enabled": task.enabled,
        "message": f"Task '{task.name}' has been {status_text}"
    })
