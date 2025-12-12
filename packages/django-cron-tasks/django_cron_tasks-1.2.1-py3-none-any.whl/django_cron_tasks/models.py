from django.db import models


class TaskResult(models.Model):
    name = models.CharField(max_length=250)

    args = models.JSONField(null=True, default=None)
    kwargs = models.JSONField(null=True, default=None)

    # When task result was created, either by scheduler, or by somebody manually starting the script
    created_at = models.DateTimeField(auto_now_add=True)

    # If this task was created periodically
    started_by_scheduler = models.BooleanField(null=True, default=None)

    # The actual run times
    started_at = models.DateTimeField(null=True, default=None)
    finished_at = models.DateTimeField(null=True, default=None)

    success = models.BooleanField(null=True, default=None)

    output = models.TextField()

    def __str__(self):
        return self.name

    class Meta:

        indexes = (
            models.Index(fields=('name', 'started_by_scheduler', 'created_at'), name='index_find_latest_run'),
            models.Index(fields=('created_at', 'started_at'), name='index_find_unstarted'),
        )


class DbLock(models.Model):
    name = models.CharField(max_length=250, unique=True)
    locked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
