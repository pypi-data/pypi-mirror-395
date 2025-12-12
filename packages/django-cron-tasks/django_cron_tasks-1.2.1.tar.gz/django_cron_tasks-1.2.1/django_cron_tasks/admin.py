from django.contrib import admin

from . import models

@admin.register(models.TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'started_at', 'finished_at', 'started_by_scheduler', 'success')
    readonly_fields = ('name', 'created_at', 'started_at', 'finished_at', 'started_by_scheduler', 'success', 'output')
