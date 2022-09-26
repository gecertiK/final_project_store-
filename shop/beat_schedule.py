#  Celery Scheduled Tasks

from celery.schedules import crontab

imports = ('app.main.tasks.tasks',)

BEAT_SCHEDULE = {
    'update_store_db': {
        'task': 'shop.synchronize_orders',
        # 'schedule': crontab(minute='*/2'),
        'schedule': crontab(),
    },
    'synchronize_db': {
        'task': 'synchronize_db',
        # 'schedule': crontab(hour='*/1'),
        'schedule': crontab(),
    },
}