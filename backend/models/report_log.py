from uuid import uuid4
from django.db import models
from datetime import datetime


class ReportLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = "Reports Logs"

    