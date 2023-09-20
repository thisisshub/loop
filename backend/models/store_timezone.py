from django.db import models


class StoreTimezone(models.Model):
    store_id = models.PositiveBigIntegerField(blank=True, null=True)
    timezone_str = models.CharField(max_length=255, default="America/Chicago")
    
    class Meta:
        verbose_name_plural = "Store Timezone"
    
    def __str__(self) -> str:
        return str(self.store_id)