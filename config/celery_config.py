import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from apps 
app.autodiscover_tasks(related_name='tasks')


app.conf.broker_transport_options = {
    'priority_steps': list(range(2)),
    'sep': ':',
    'queue_order_strategy': 'priority',
}

app.conf.task_acks_late = True 
app.conf.task_default_priority = 1
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1