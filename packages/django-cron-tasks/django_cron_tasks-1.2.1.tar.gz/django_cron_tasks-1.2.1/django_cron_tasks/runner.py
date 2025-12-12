import json

from django_cron_tasks import models


def run_task(name, *args, **kwargs):

    # Make sure args and kwargs are JSON serializable
    if args:
        try:
            json.dumps(args)
        except (TypeError, OverflowError):
            raise RuntimeError('Contains arguments that are not JSON serializable!')
    if kwargs:
        try:
            json.dumps(kwargs)
        except (TypeError, OverflowError):
            raise RuntimeError('Contains key word arguments that are not JSON serializable!')

    return models.TaskResult.objects.create(
        name=name,
        args=args,
        kwargs=kwargs,
        started_by_scheduler=False,
    )
