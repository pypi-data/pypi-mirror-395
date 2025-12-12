Django Cron Tasks
=================

Django background tasks, ran via crontab.


How to use
==========

1. Install:

    ```
    pip install django-cron-tasks
    ```

2. Add to `settings.py`:

    ```
    INSTALLED_APPS = [
        ...
        'django_cron_tasks',
        ...
    ]

    DJANGO_CRON_TASKS = [
        {
            'task': 'your.module.your_function',
            'schedule': datetime.timedelta(hours=6),
        },
    ]
    ```

3. Apply migrations

    ```
    ./manage.py migrate
    ```

4. Add this to your crontab:

    ```
    * * * * * cd /your_project/ && /path_to_your_venv/bin/python manage.py run_cron_tasks
    ```
