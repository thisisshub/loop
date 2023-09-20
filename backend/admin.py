from backend import models
from django.contrib import admin


class StoreActivityAdminView(admin.ModelAdmin):
    list_display = ["store_id", "status", "timestamp"]
    list_filter = ["status"]
    search_fields = ["store_id"]
    _fields = [field.upper() for field in search_fields]
    search_help_text = f"Search fields allowed: {', '.join(_fields)}"

class BusinessHoursAdminView(admin.ModelAdmin):
    list_display = ["store_id", "start_time_local", "end_time_local"]
    list_filter = ["day_of_the_week"]
    search_fields = ["store_id"]
    _fields = [field.upper() for field in search_fields]
    search_help_text = f"Search fields allowed: {', '.join(_fields)}"

class StoreTimezoneAdminView(admin.ModelAdmin):
    list_display = ["store_id", "timezone_str"]
    list_filter = ["timezone_str"]
    search_fields = ["store_id"]
    _fields = [field.upper() for field in search_fields]
    search_help_text = f"Search fields allowed: {', '.join(_fields)}"

class ReportAdminView(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]
    _fields = [field.upper() for field in search_fields]
    search_help_text = f"Search fields allowed: {', '.join(_fields)}"

class ReportLogAdminView(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]
    _fields = [field.upper() for field in search_fields]
    search_help_text = f"Search fields allowed: {', '.join(_fields)}"


admin.site.register(models.ReportGeneration, ReportAdminView)
admin.site.register(models.ReportLog, ReportAdminView)
admin.site.register(models.StoreActivity, StoreActivityAdminView)
admin.site.register(models.BusinessHours, BusinessHoursAdminView)
admin.site.register(models.StoreTimezone, StoreTimezoneAdminView)