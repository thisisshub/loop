# Core
import pytz
import pandas as pd
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from django.core.files.base import File

# Celery
from celery import shared_task
from celery.utils.log import get_task_logger

# Models
from backend import models
from backend import serializer

logger = get_task_logger(__name__)

@shared_task
def update_store_status():
    csv_data = pd.read_csv("./csv_data/store status.csv")
    for data in csv_data.to_dict("records"):
        try:
            models.StoreActivity.objects.create(
                    store_id=data.get("store_id"),
                    status=data.get("status"),
                    timestamp=datetime.strptime(data.get("timestamp_utc"), '%Y-%m-%d %H:%M:%S.%f %Z').replace(tzinfo=timezone.utc)
                )
        except:
            logger.error(f"Could not store entry for store_id {data.get('store_id')}")
            continue

@shared_task
def update_business_hours():
    csv_data = pd.read_csv("./csv_data/Menu hours.csv")
    for data in csv_data.to_dict("records"):
        models.BusinessHours.objects.create(
                store_id=data.get("store_id"),
                day_of_the_week=int(data.get("day")),
                start_time_local=data.get("start_time_local"),
                end_time_local=data.get("end_time_local")
            )
        try:
            pass
        except:
            logger.error(f"Could not store entry for store_id {data.get('store_id')}")
            continue

@shared_task
def update_store_timezones():
    csv_data = pd.read_csv("./csv_data/bq-results-20230125-202210-1674678181880.csv")
    for data in csv_data.to_dict("records"):
        models.StoreTimezone.objects.create(
                store_id=data.get("store_id"), 
                timezone_str=data.get("timezone_str")
            )
        try:
            pass
        except:
            logger.error(f"Could not store entry for store_id {data.get('store_id')}")
            continue


@shared_task
def generate_report(report_id: str):
    """
    Generates a report containing store performance metrics based on store activity and business hours data.

    Args:
        report_id (str): The identifier for the generated report.

    Steps:
    1. Fetch store timezone, business hours, and store activity data from the database.
    2. Convert the fetched data into Pandas DataFrames for efficient processing.
    3. Initialize an empty list to store the metrics for each store.
    4. Iterate over each store's data to calculate metrics:
       - Filter activity data for the current store_id.
       - Determine the store's timezone.
       - Calculate the current time in the local timezone.
       - Calculate time ranges for the last hour, last day, and last week.
       - Filter business hours data that falls within these time ranges.
       - Calculate the total duration of valid business hours and active time within each time range.
       - Calculate uptime (in minutes) and downtime (in minutes) for each time range.
    5. Handle cases where a 'store_id' does not exist in the data by continuing to the next store.
    6. Store the calculated metrics in a list.
    7. Create a Pandas DataFrame to store the results.
    8. Save the DataFrame as a CSV file with a filename based on the 'report_id'.
    9. Open and wrap the CSV file as a Django File object.
    10. Serialize and save the File object as a report file using the 'ReportFileSerializer'.
    
    Note:
    - The 'report_id' is used as a unique identifier for the generated report and in the filename.
    """
    store_timezone = serializer.StoreTimezoneSerializer(models.StoreTimezone.objects.all(), many=True)
    store_business_hours = serializer.BusinessHoursSerializer(models.BusinessHours.objects.all(), many=True)
    store_activity = serializer.StoreActivitySerializer(models.StoreActivity.objects.all(), many=True)

    store_timezone_df = pd.DataFrame(store_timezone.data)
    store_business_hours_df = pd.DataFrame(store_business_hours.data)
    store_activity_df = pd.DataFrame(store_activity.data)
    
    metrics_list = []
    for store_id in store_activity_df['store_id']:
        try:
            # Filter activity data for the current store_id.
            store_activity_subset = store_activity_df[store_activity_df['store_id'] == store_id]
            
            # Get the corresponding timezone for the current store_id.
            store_timezone = store_timezone_df[store_timezone_df['store_id'] == store_id]['timezone_str'].iloc[0]
            local_timezone = pytz.timezone(store_timezone)
            
            # Calculate the current time in the local timezone.
            current_time_local = datetime.now(local_timezone)
            
            # Calculate the start time of the last hour in the local timezone.
            last_hour_start_time = current_time_local - timedelta(hours=1)
            last_day_start_time = current_time_local - timedelta(days=1)
            last_week_start_time = current_time_local - timedelta(weeks=1)

            # Filter business hours data for the current store_id.
            store_business_hours_subset = store_business_hours_df[store_business_hours_df['store_id'] == store_id]

            # Convert start_time_local and end_time_local to datetime objects in the local timezone.
            store_business_hours_subset['start_time_local'] = pd.to_datetime(store_business_hours_subset['start_time_local']).apply(lambda x: local_timezone.localize(x))
            store_business_hours_subset['end_time_local'] = pd.to_datetime(store_business_hours_subset['end_time_local']).apply(lambda x: local_timezone.localize(x))

            # Filter business hours that fall within the last hour, last day, and last week.
            valid_business_hours_hour = store_business_hours_subset[
                (store_business_hours_subset['start_time_local'].dt.to_pydatetime() <= last_hour_start_time) &
                (store_business_hours_subset['end_time_local'].dt.to_pydatetime() >= current_time_local)
            ]

            valid_business_hours_day = store_business_hours_subset[
                (store_business_hours_subset['start_time_local'].dt.to_pydatetime() <= last_day_start_time) &
                (store_business_hours_subset['end_time_local'].dt.to_pydatetime() >= current_time_local)
            ]

            valid_business_hours_week = store_business_hours_subset[
                (store_business_hours_subset['start_time_local'].dt.to_pydatetime() <= last_week_start_time) &
                (store_business_hours_subset['end_time_local'].dt.to_pydatetime() >= current_time_local)
            ]

            # Calculate the total duration of valid business hours in the last hour, last day, and last week.
            total_duration_hour = valid_business_hours_hour['end_time_local'].sub(valid_business_hours_hour['start_time_local']).sum()
            total_duration_day = valid_business_hours_day['end_time_local'].sub(valid_business_hours_day['start_time_local']).sum()
            total_duration_week = valid_business_hours_week['end_time_local'].sub(valid_business_hours_week['start_time_local']).sum()

            # Calculate the total duration of active time in the last hour, last day, and last week.
            active_duration_hour = timedelta()
            active_duration_day = timedelta()
            active_duration_week = timedelta()

            for index, activity in store_activity_subset.iterrows():
                activity_timestamp = pd.to_datetime(activity['timestamp'])
                if last_hour_start_time <= activity_timestamp <= current_time_local:
                    active_duration_hour += timedelta(minutes=1)  # Assuming each activity lasts for 1 minute.
                if last_day_start_time <= activity_timestamp <= current_time_local:
                    active_duration_day += timedelta(days=1)
                if last_week_start_time <= activity_timestamp <= current_time_local:
                    active_duration_week += timedelta(weeks=1)

            # Calculate the uptime_last_hour (in minutes) and handle division by zero
            if total_duration_hour.total_seconds() > 0:
                uptime_last_hour = active_duration_hour.total_seconds() / 60
            else:
                uptime_last_hour = 0.0  # Set to 0 minutes if no valid business hours

            # Calculate the uptime_last_day (in minutes) and handle division by zero
            if total_duration_day.total_seconds() > 0:
                uptime_last_day = active_duration_day.total_seconds() / 3600
            else:
                uptime_last_day = 0.0  # Set to 0 minutes if no valid business hours during the day

            # Calculate the uptime_last_week (in minutes) and handle division by zero
            if total_duration_week.total_seconds() > 0:
                uptime_last_week = active_duration_week.total_seconds() / 3600
            else:
                uptime_last_week = 0.0  # Set to 0 minutes if no valid business hours during the week

            # Calculate downtime
            downtime_last_hour = total_duration_hour.total_seconds() / 60 - uptime_last_hour
            downtime_last_day = total_duration_day.total_seconds() / 3600 - uptime_last_day
            downtime_last_week = total_duration_week.total_seconds() / 3600 - uptime_last_week

            metrics_list.append({
                'store_id': store_id,
                'uptime_last_hour': uptime_last_hour,
                'uptime_last_day': uptime_last_day,
                'uptime_last_week': uptime_last_week,
                'downtime_last_hour': downtime_last_hour,
                'downtime_last_day': downtime_last_day,
                'downtime_last_week': downtime_last_week
            })
        except:
            # Handle cases where a store_id does not exist in one of the DataFrames.
            # print(f"Skipping store_id {store_id} because it doesn't exist in one of the DataFrames.")
            continue

    # Create a DataFrame to store the results.
    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv(f"./temp/files/temp_{report_id}.csv")

    with open(f"./temp/files/temp_{report_id}.csv", "rb") as report:
        wrapped_report = File(report)
        report_serializer = serializer.ReportFileSerializer(data={"report_file": wrapped_report})
        report_serializer.is_valid(raise_exception=True)
        report_serializer.save()

    