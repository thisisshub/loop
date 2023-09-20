from django.db import models
from datetime import datetime

class StoreActivity(models.Model):
    status_choices = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    store_id = models.PositiveBigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=status_choices, default="inactive", null=False, blank=False)
    timestamp = models.DateTimeField(blank=True, null=True, default=datetime.now)

    class Meta:
        verbose_name_plural = "Store Activity"

    def __str__(self) -> str:
        return str(self.store_id)