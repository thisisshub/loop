# Django
from django.urls import path

# Views
from .views import GetReport
from .views import TriggerReport

urlpatterns = [
    path("trigger_report/", TriggerReport.as_view(), name="api_trigger_report"),
    path("get_report/", GetReport.as_view(), name="api_trigger_report")
]
