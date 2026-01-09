from ai_admin.models import TaskLog

def get_chat_history(limit: int = 10, offset: int = 0):
    """
    Retrieves the chat history from TaskLog objects.
    Returns a list of user requests and agent responses.
    """
    tasks = TaskLog.objects.all().order_by('-created_at')[offset:offset+limit]
    history = []
    for task in reversed(tasks):
        history.append({
            "role": "user",
            "content": task.user_request
        })
        if task.result_summary:
            history.append({
                "role": "assistant",
                "content": task.result_summary
            })
        elif task.error_message:
            history.append({
                "role": "assistant",
                "content": f"Error: {task.error_message}"
            })
    return history

def get_task_list(limit: int = 10, offset: int = 0):
    """
    Retrieves a summary list of tasks.
    """
    tasks = TaskLog.objects.all().order_by('-created_at')[offset:offset+limit]
    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.id,
            "created_at": task.created_at.isoformat(),
            "status": task.status,
            "user_request_snippet": task.user_request[:50] + "..." if len(task.user_request) > 50 else task.user_request
        })
    return task_list

def get_task_details(task_id: int):
    """
    Retrieves detailed information about a specific task.
    """
    try:
        task = TaskLog.objects.get(id=task_id)
        details = {
            "id": task.id,
            "created_at": task.created_at.isoformat(),
            "status": task.status,
            "user_request": task.user_request,
            "result_summary": task.result_summary,
            "error_message": task.error_message,
            "current_agent": task.current_agent,
            "report_slug": task.report.slug if hasattr(task, 'report') else None
        }
        return details
    except TaskLog.DoesNotExist:
        return {"error": f"Task with ID {task_id} not found."}
