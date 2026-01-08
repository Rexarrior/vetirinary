from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import TaskLog, TaskReport

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def task_status(request, task_id):
    """
    API endpoint to check the status of a task.
    """
    task = get_object_or_404(TaskLog, id=task_id)
    return JsonResponse({
        'id': task.id,
        'status': task.status,
        'current_agent': task.current_agent,
        'result_summary': task.result_summary,
        'error_message': task.error_message,
    })

@user_passes_test(is_superuser)
def view_report(request, slug):
    """
    View to render the HTML report for a task.
    """
    report = get_object_or_404(TaskReport, slug=slug)
    return render(request, 'ai_admin/report.html', {'report': report})
