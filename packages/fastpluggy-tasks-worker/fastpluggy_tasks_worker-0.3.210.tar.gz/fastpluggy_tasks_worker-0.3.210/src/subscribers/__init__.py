import logging

from .telemetry import TaskTelemetry
from ..config import TasksRunnerSettings

from .db_adapter import DBPersistence
from .metrics import MetricsPersistence


def create_tables_for_save(settings):
    if settings.store_task_db:
        from fastpluggy.core.database import create_table_if_not_exist

        from ..persistence.models.context import TaskContextDB
        create_table_if_not_exist(TaskContextDB)
        from ..persistence.models.report import TaskReportDB
        create_table_if_not_exist(TaskReportDB)

        if settings.scheduler_enabled:
            from ..persistence.models.scheduled import ScheduledTaskDB
            create_table_if_not_exist(ScheduledTaskDB)

        return True
    return False

def setup_persistence(bus):
    # Create and register persistence listener
    settings = TasksRunnerSettings()

    # Always register metrics persistence (no-op if prometheus_client missing)
    try:
        bus.subscribe_class(MetricsPersistence)
    except Exception as e:
        logging.exception(f"Failed to register metrics persistence: {e}")

    # Always register in-memory telemetry (very cheap, no deps)
    try:
            bus.subscribe_class(TaskTelemetry)
    except Exception as e:
            logging.exception(f"Failed to register task telemetry: {e}")

    if create_tables_for_save(settings=settings):
        bus.subscribe_class(DBPersistence)  # auto-wires all on_<status> methods


    # Optionally return the bus for wiring
    return bus