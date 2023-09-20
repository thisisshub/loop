from __future__ import absolute_import
from __future__ import unicode_literals

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loop.settings")
app = Celery("loop")
app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
