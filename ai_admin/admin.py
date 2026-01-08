from django.contrib import admin
from .models import TaskLog, TaskReport

@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'current_agent', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_request', 'result_summary', 'error_message')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TaskReport)
class TaskReportAdmin(admin.ModelAdmin):
    list_display = ('task', 'slug', 'created_at')
    search_fields = ('slug', 'task__user_request')
    readonly_fields = ('created_at',)
