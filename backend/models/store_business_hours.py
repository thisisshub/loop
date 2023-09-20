from django.db import models
from datetime import datetime


class BusinessHours(models.Model):
    days = [
        (i, j) for i, j in zip(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ]
    store_id = models.PositiveBigIntegerField(blank=True, null=True)
    day_of_the_week = models.CharField(max_length=11, choices=days, default=0, editable=True, blank=False, null=False)
    start_time_local = models.TimeField(default=datetime.now, blank=True, null=True)
    end_time_local = models.TimeField(default=datetime.now, null=True, blank=True, editable=True)
    
    class Meta:
        verbose_name_plural = "Business Hours"

    def __str__(self) -> str:
        return str(self.store_id)