from backend import models
from rest_framework.serializers import ModelSerializer

class StoreActivitySerializer(ModelSerializer):
    class Meta:
        model = models.StoreActivity
        fields = "__all__"


class BusinessHoursSerializer(ModelSerializer):
    class Meta:
        model = models.BusinessHours
        fields = "__all__"


class StoreTimezoneSerializer(ModelSerializer):
    class Meta:
        model = models.StoreTimezone
        fields = "__all__"


class ReportFileSerializer(ModelSerializer):
    class Meta:
        model = models.ReportGeneration
        fields = "__all__"


class ReportLogSerializer(ModelSerializer):
    class Meta:
        model = models.ReportLog
        fields = "__all__"