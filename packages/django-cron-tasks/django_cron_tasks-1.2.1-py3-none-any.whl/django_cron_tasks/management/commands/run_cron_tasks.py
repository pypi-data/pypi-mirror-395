import importlib
import io
import sys
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django_cron_tasks import models
from django_cron_tasks.lock import Lock


class Command(BaseCommand):
    help = 'Runs background tasks.'

    def handle(self, *args, **options):

        # First create TaskResult objects by scheduler
        lock = Lock('django_cron_tasks_scheduler', block=False, raise_exception=False)
        try:
            if lock.acquire():
                for task in getattr(settings, 'DJANGO_CRON_TASKS', []):
                    latest_run = models.TaskResult.objects.filter(name=task['task']).filter(started_by_scheduler=True).order_by('created_at').last()
                    # TODO: Support crontab like syntax too!
                    if not latest_run or latest_run.created_at + task['schedule'] < timezone.now():

                        # Create a new entry to database
                        # TODO: Support giving arguments!
                        result = models.TaskResult.objects.create(
                            name=task['task'],
                            started_by_scheduler=True,
                        )
        finally:
            lock.release()

        # Now run all the tasks that are waiting for running
        while True:

            # Get the oldest task that has not been started yet.
            result = models.TaskResult.objects.filter(started_at=None).order_by('created_at').first()

            # If there are no task, then stop
            if not result:
                break

            # Try to "lock" this task for this runner
            if models.TaskResult.objects.filter(id=result.id, started_at=None).update(started_at=timezone.now()):

                # Get function
                task_splitted = result.name.split('.')
                module_path = '.'.join(task_splitted[0:-1])
                func_name = task_splitted[-1]
                module = importlib.import_module(module_path)
                func = getattr(module, func_name)

                # Get arguments
                args = result.args or []
                kwargs = result.kwargs or {}

                # Run it
                func_output = io.StringIO()
                default_stdout = sys.stdout
                default_stderr = sys.stderr
                sys.stdout = func_output
                sys.stderr = func_output
                try:
                    func(*args, **kwargs)
                except Exception as err:
                    # Mark task failed
                    result.finished_at = timezone.now()
                    result.success = False
                    result.output = func_output.getvalue() + traceback.format_exc()
                    # Also reset arguments for security reasons
                    result.args = None
                    result.kwargs = None
                    result.save(update_fields=('finished_at', 'success', 'output', 'args', 'kwargs'))
                    # Try the next task
                    continue
                finally:
                    sys.stdout = default_stdout
                    sys.stderr = default_stderr

                # Mark task finished successfully
                result.finished_at = timezone.now()
                result.success = True
                result.output = func_output.getvalue()
                # Also reset arguments for security reasons
                result.args = None
                result.kwargs = None
                result.save(update_fields=('finished_at', 'success', 'output', 'args', 'kwargs'))
