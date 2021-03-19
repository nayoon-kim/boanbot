import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boanbot.settings')

from django.conf import settings
from tasks import crawling_process

app = Celery("boanbot")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule={
        'crawling_process-an-hour': {
            'task': 'crawling_process',
            'schedule': timedelta(seconds=600),
            'args': (),
        },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
