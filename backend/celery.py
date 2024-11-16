from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# app = Celery('backend')
app = Celery('backend', broker='redis://:yKlVkKdFbCQceLf3wk0QZ0afA7a719fu@redis-10915.c257.us-east-1-3.ec2.redns.redis-cloud.com:10915/0')
app.conf.result_backend = 'redis://:yKlVkKdFbCQceLf3wk0QZ0afA7a719fu@redis-10915.c257.us-east-1-3.ec2.redns.redis-cloud.com:10915/0'


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')