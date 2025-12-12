/**
 * Utilities for loading available tasks and updating the task form based on selection.
 * These functions rely on window.TASK_FORM_CONFIG:
 *   - url_list_available_tasks: string
 *   - availableTasks: array (filled after load)
 */

function updateTaskFormFromSelectionGeneric(selectId, paramsContainerId, topicInputId, existingArgs) {
  try {
    const selectEl = document.getElementById(selectId);
    if (!selectEl) return;

    const selected = selectEl.value;
    const taskMeta = (window.TASK_FORM_CONFIG?.availableTasks || []).find(t => t.name === selected);

    if (paramsContainerId) {
      if (taskMeta && taskMeta.params) {
        renderTaskForm(paramsContainerId, taskMeta.params);
        // Prefill values from existingArgs if provided
        if (existingArgs && typeof existingArgs === 'object') {
          try {
            Object.entries(existingArgs).forEach(([k, v]) => {
              const el = document.querySelector(`#${paramsContainerId} [name="${k}"]`);
              if (!el) return;
              if (el.type === 'checkbox') {
                el.checked = Boolean(v);
              } else {
                el.value = v;
              }
            });
          } catch (e) { /* ignore prefill errors */ }
        }
      } else {
        const container = document.getElementById(paramsContainerId);
        if (container) container.innerHTML = "<p class='text-muted'>No parameters required.</p>";
      }
    }

    if (topicInputId) {
      const topicInput = document.getElementById(topicInputId);
      if (topicInput) {
        const def = (taskMeta && taskMeta.topic) ? taskMeta.topic : "";
        topicInput.value = def || "";
      }
    }
  } catch (err) {
    console.error('updateTaskFormFromSelectionGeneric error', err);
  }
}

async function loadAvailableTasksGeneric(selectId, paramsContainerId, topicInputId, defaultSelected) {
  try {
    const url = window.global_var && window.global_var['url_list_available_tasks'];
    if (!url) {
      console.warn('No URL for available tasks. Expected window.global_var.url_list_available_tasks');
      return;
    }

    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch tasks');

    const tasks = await response.json();
    window.TASK_FORM_CONFIG = Object.assign({}, window.TASK_FORM_CONFIG, {
      availableTasks: tasks,
      defaultTask: tasks.length > 0 ? tasks[0].name : ''
    });

    // Group tasks by module/package
    const tasksByPackage = {};
    tasks.forEach(task => {
      const pkg = task.module || 'unknown';
      if (!tasksByPackage[pkg]) tasksByPackage[pkg] = [];
      tasksByPackage[pkg].push(task);
    });

    const selectElement = document.getElementById(selectId);
    if (selectElement) {
      const wanted = defaultSelected || selectElement.value || window.TASK_FORM_CONFIG.defaultTask || '';
      selectElement.innerHTML = '';
      Object.entries(tasksByPackage).forEach(([pkg, pkgTasks]) => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = pkg;
        pkgTasks.forEach(task => {
          const option = document.createElement('option');
          option.value = task.name;
          option.textContent = `${task.name} – ${task.description || task.qualified_name || ''}`;
          if (task.name === wanted) option.selected = true;
          optgroup.appendChild(option);
        });
        selectElement.appendChild(optgroup);
      });
    }

    updateTaskFormFromSelectionGeneric(selectId, paramsContainerId, topicInputId);
  } catch (error) {
    console.error('Error loading available tasks:', error);
  }
}
