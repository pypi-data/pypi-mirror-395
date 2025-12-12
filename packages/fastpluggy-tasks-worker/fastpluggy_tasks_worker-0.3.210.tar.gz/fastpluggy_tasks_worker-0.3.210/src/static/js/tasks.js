/**
 * Format duration with appropriate units (ms, s, m, h)
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration string
 */
function formatDuration(seconds) {
    if (seconds == null || isNaN(seconds)) return "-";

    // Less than 1 second: show milliseconds
    if (seconds < 1) {
        const ms = Math.round(seconds * 1000);
        return `${ms} ms`;
    }

    // Less than 60 seconds: show seconds with 2 decimals
    if (seconds < 60) {
        return `${seconds.toFixed(2)} s`;
    }

    // Less than 1 hour: show minutes and seconds
    if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.round(seconds % 60);
        return `${minutes} m ${secs} s`;
    }

    // Less than 1 day: show hours, minutes, and seconds
    if (seconds < 86400) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.round(seconds % 60);
        return `${hours} h ${minutes} m ${secs} s`;
    }

    // 1 day or more: show days and hours
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    return `${days} d ${hours} h`;
}

// Function to submit tasks to the task system
// Added optional callback parameter. If not provided, a default notification will be shown
// with a link to the created task's details (if available).
async function submitTask(taskFunction, taskName, taskParams, callback) {
    // Ensure kwargs is a plain object; backend expects a dict, not a string
    let kwargs = taskParams;
    if (typeof kwargs === 'string') {
        try {
            const parsed = JSON.parse(kwargs);
            kwargs = (parsed && typeof parsed === 'object') ? parsed : {};
        } catch (e) {
            kwargs = {};
        }
    } else if (!kwargs || typeof kwargs !== 'object') {
        kwargs = {};
    }

    const response = await fetch(window.global_var['task_submit_url']+'?method=json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            function: taskFunction,
            name: taskName,
            kwargs: kwargs
        })
    });

    const data = await response.json();

    // Default callback: notify user with link to task details (similar to flash message)
    try {
        if (typeof callback === 'function') {
            callback(data);
        } else {
            const hasShowNotification = typeof window.showNotification === 'function';
            const detailsTpl = window.global_var && window.global_var['url_task_details'];
            const taskId = data && data.task_id;
            let link = null;
            if (detailsTpl && taskId) {
                link = detailsTpl.replace('TASK_ID_REPLACE', taskId);
            }
            const isOk = !!taskId;
            const message = isOk
                ? (data && data.message) || `Task "${taskName}" queued successfully.`
                : (data && data.message) || `Failed to queue task "${taskName}".`;

            if (hasShowNotification) {
                // websocket_tool/scripts.js signature: showNotification(message, level, link?)
                window.showNotification(message, isOk ? 'success' : 'error', link || undefined);
            } else {
                // Fallback to alert
                const fullMsg = link ? `${message}\n${link}` : message;
                try { alert(fullMsg); } catch (_) { /* noop */ }
            }
        }
    } catch (e) {
        // Do not block the caller if notification fails
        console.error('submitTask default callback failed:', e);
    }

    // Always return the response data for chaining/back-compat
    return data;
}