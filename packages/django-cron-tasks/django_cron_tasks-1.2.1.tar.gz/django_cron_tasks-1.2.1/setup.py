#!/usr/bin/env python
from setuptools import setup

setup(
    name='django_cron_tasks',
    description='Django background tasks, ran via crontab.',
    version='1.2.1',
    packages=[
        'django_cron_tasks',
        'django_cron_tasks.management',
        'django_cron_tasks.management.commands',
        'django_cron_tasks.migrations',
    ],
    author='Henrik Heino',
    author_email='henrik.heino@gmail.com',
    license='MIT License',
    url='https://github.com/henu/django_cron_tasks',
)
