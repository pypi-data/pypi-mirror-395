from typing import Optional, Dict, Any, Callable

from fastpluggy.core.widgets import BaseButtonWidget, RequestParamsMixin
from starlette.requests import Request

from ..core.utils import func_to_path
from fastpluggy.core.tools.serialize_tools import serialize_value
from ..core.topic import resolve_topic


class RunTaskButtonWidget(BaseButtonWidget, RequestParamsMixin):
    """
    Simple button widget with URL navigation.
    """

    widget_type = "button"

    request: Request | None = None

    def __init__(
            self,
            task: str | Callable,
            task_kwargs: Optional[dict] = {},
            redirect_to_detail: bool = False,
            topic: Optional[str] = None,
            topic_editable: bool = False,
            **kwargs
    ):
        """
        Initialize button widget.

        Args:
            url: Target URL (supports placeholders like <field_name>)
        """
        super().__init__(**kwargs)
        self.url = "#"
        self.task = task
        self.redirect_to_detail = redirect_to_detail
        # Normalize task using shared utility
        self._task_name = func_to_path(task)
        self.task_kwargs = task_kwargs
        self.topic = topic
        self.topic_editable = topic_editable

    def process(self, item: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Process button data."""

        url_submit_task = self.request.url_for("submit_task")
        url_detail_task = self.request.url_for("task_details", task_id="__TASK_ID_REPLACE__")

        for key, value in self.task_kwargs.items():
            if isinstance(value, str):
                self.task_kwargs[key] = self.replace_placeholders(self.task_kwargs[key], item=item)
            elif isinstance(value, bool):
                self.task_kwargs[key] = str(self.task_kwargs[key]).lower()

        default_topic = resolve_topic(self.task, self.topic)
        default_topic_js = default_topic
        editable_js = str(self.topic_editable).lower()

        full_payload = {
            "function": self._task_name,
            "kwargs": serialize_value(self.task_kwargs),
        }
        payload_str = full_payload

        js = f"""
           (async () => {{
                const params = {payload_str}.kwargs || {{}};
                const taskFunction = '{self._task_name}';
                const taskName = '{self.label or self._task_name}';
                const defaultTopic = '{default_topic_js}';
                let topicVal = defaultTopic;
                if ({editable_js}) {{
                    const userInput = window.prompt('Topic for this task', defaultTopic);
                    if (userInput === null) return; // cancel
                    topicVal = userInput;
                }}
                // Try to pass topic via params so backend can use/override if supported
                if (topicVal) {{
                    try {{ params.topic = topicVal; }} catch (_) {{ /* ignore */ }}
                }}
                try {{
                    await submitTask(taskFunction, taskName, params);
                }} catch (err) {{
                    console.error(err);
                    alert('Network error. Please try again.');
                }}
           }})();
           """

        self.onclick = js
        if self.label is None:
            self.label = f"Run Task {self._task_name}"
