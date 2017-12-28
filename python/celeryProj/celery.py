# -*- coding: utf8 -*-
from celery import Celery
from kombu import Queue, Exchange
from kombu.common import Broadcast
from datetime import timedelta
import random

app = Celery('proj', broker='amqp://guest:guest@localhost')

topicExchange = Exchange('helloEx', type='topic')

app.conf.update(
    CELERY_IMPORTS='celeryProj.tasks',
    CELERY_ROUTES={
        'celeryProj.tasks.add': {'queue': 'add'},
        'celeryProj.tasks.mul': {'queue': 'mul'},
        'celeryProj.tasks.hello': {
            'queue': 'broadcast_tasks',
            # 'routing_key': 'hello.h',
            "exchange": "broadcast_tasks",
            # "exchange_type": "topic",
        },
        'celeryProj.tasks.hello2': {
            'queue': 'broadcast_tasks',
            "exchange": "broadcast_tasks",
        },
    },
    CELERYBEAT_SCHEDULE={
        "add-every-30-seconds": {
            "task": "celeryProj.tasks.hello",
            "schedule": timedelta(seconds=30)
        }
    },
    CELERY_TIMEZONE="Asia/Shanghai",
    CELERY_QUEUES=(
        Queue('add'),
        Queue('mul'),
        # Queue('hello.%d' % random.randint(0, 100), exchange=topicExchange, routing_key='hello.*'),
        Broadcast('broadcast_tasks')
    )
)


if __name__ == '__main__':
    app.start()
