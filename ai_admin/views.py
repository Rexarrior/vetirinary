from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import TaskLog, TaskReport
from .tasks import start_admin_task
import json
from django.views.decorators.csrf import csrf_exempt

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
        'report_slug': task.report.slug if hasattr(task, 'report') else None,
    })

@user_passes_test(is_superuser)
def view_report(request, slug):
    """
    View to render the HTML report for a task.
    """
    report = get_object_or_404(TaskReport, slug=slug)
    return render(request, 'ai_admin/report.html', {'report': report})

@user_passes_test(is_superuser)
def admin_dashboard(request):
    """
    Renders the AI Admin Dashboard.
    """
    return render(request, 'ai_admin/dashboard.html')

@user_passes_test(is_superuser)
@csrf_exempt
def api_chat(request):
    """
    API to create a new task from a user message.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)

            # Create TaskLog
            task = TaskLog.objects.create(
                user_request=message,
                status='pending'
            )

            # Trigger Celery task
            start_admin_task.delay(task.id)

            return JsonResponse({
                'id': task.id,
                'status': task.status,
                'created_at': task.created_at.isoformat()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@user_passes_test(is_superuser)
def api_task_list(request):
    """
    API to retrieve the list of tasks.
    """
    tasks = TaskLog.objects.all().values(
        'id', 'user_request', 'status', 'created_at', 'current_agent', 'result_summary'
    )
    return JsonResponse({'tasks': list(tasks)})
