import json
import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone


class Event:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.model = kwargs.get('model')
        self.data = kwargs.get('data')
        self.cloud_tasks = []
        self.d = None

    def add_task(self, **kwargs):
        d = {
            "queue": kwargs.get('queue', 'cloud-tasks-default'),
            "http_request": {
                "http_method": kwargs.get('http_method', 'POST'),
                "url": kwargs.get('url'),
                "body": kwargs.get('json', {}),
            },
        }
        if kwargs.get('delay_in_minutes') is not None:
            d['start_at'] = (timezone.now() + timedelta(minutes=int(kwargs.get('delay_in_minutes', 0)))).isoformat()
        self.cloud_tasks.append(d)

    def save(self):
        pass

    def fire(self, **kwargs):
        gid = getattr(self.model, "gid", None)

        def add_debug_id(cloud_task, span):
            if span is None:
                return cloud_task
            cloud_task['http_request']['headers'] = {
                'Debug-ID': f'{span.id}',
            }
            return cloud_task

        self.d = {
            "name": self.name,
            "env": "develop" if settings.DEBUG else "production",
            "gid": gid,
            "data": self.data,
            "cloud-tasks": [add_debug_id(task, kwargs.get('trace')) for task in self.cloud_tasks],
        }
        if kwargs.get('trace') is not None:
            self.d['trace_id'] = kwargs.get('trace').id
        self.save()
        try:
            logging.info('event-fire {}'.format(json.dumps(self.d)))
        except Exception:
            raise Exception('event convert to json error') # noqa: B904
