import os
import django
import sys
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic.settings')
django.setup()

from ai_admin.models import TaskLog, TaskReport
from ai_admin.tasks import start_admin_task

def test_admin_workflow():
    print("Creating test TaskLog...")
    task_log = TaskLog.objects.create(
        user_request="Test request for AI Admin",
        status='pending'
    )
    print(f"TaskLog created: {task_log.id}")

    print("Starting admin task (synchronously)...")
    start_admin_task(task_log.id)

    # Refresh from DB
    task_log.refresh_from_db()
    print(f"Final Task Status: {task_log.status}")
    print(f"Result Summary: {task_log.result_summary}")

    if task_log.status == 'completed':
        try:
            report = task_log.report
            print(f"Report generated: {report.slug}")
            print("Verification SUCCESS")
        except TaskReport.DoesNotExist:
            print("Verification FAILED: Report not generated")
    else:
        print(f"Verification FAILED: Task status is {task_log.status}")
        print(f"Error: {task_log.error_message}")

if __name__ == "__main__":
    test_admin_workflow()
