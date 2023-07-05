from __future__ import absolute_import
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_shop.settings')

app = Celery("fruit_shop", broker='redis://localhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['users', 'bank', 'fruits'])


app.conf.beat_schedule = {
    'subscription': {
        'task': 'users.tasks.test',
        # 'schedule': crontab(hour=0),
        'schedule': crontab(),
    },

}