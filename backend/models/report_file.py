from uuid import uuid4
from django.db import models
from datetime import datetime
from .report_log import ReportLog

def upload_path(instance, filename):
    return f"{'report_csv_' + str(instance.id)}.csv"

class ReportGeneration(models.Model):
    id = models.ForeignKey(ReportLog, primary_key=True, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to=upload_path)

    class Meta:
        verbose_name_plural = "Report Files"

    