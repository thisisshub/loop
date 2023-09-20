
## Project Structure

The project includes Celery tasks for handling store-related data and generating store performance reports. Below are the main components of the project structure:

- **Core Modules**: These modules contain core functionalities and utility functions.
  - `pytz`, `pandas`, `datetime`, `timezone`, and `timedelta` from Python's standard library are used for datetime and timezone operations.
  - `django.core.files.base.File` is used to work with files in Django.

- **Celery Tasks**: The project utilizes Celery for asynchronous task execution. Celery tasks are defined in this section.

- **Models**: Django models for storing store-related data are defined in the `backend.models` module.

- **Serializers**: Serializers for converting Django model data to JSON format are defined in the `backend.serializer` module.

## Celery Tasks

### Task: `update_store_status`

- Purpose: This task updates store activity status based on data from a CSV file.

- Description: The task reads data from the "store status.csv" file and creates `StoreActivity` objects in the database. Each object represents the status of a store at a specific timestamp.

### Task: `update_business_hours`

- Purpose: This task updates store business hours based on data from a CSV file.

- Description: The task reads data from the "Menu hours.csv" file and creates `BusinessHours` objects in the database. Each object represents the business hours for a store on a specific day of the week.

### Task: `update_store_timezones`

- Purpose: This task updates store timezones based on data from a CSV file.

- Description: The task reads data from the "bq-results-20230125-202210-1674678181880.csv" file and creates `StoreTimezone` objects in the database. Each object associates a store with its timezone.

### Task: `generate_report`

- Purpose: This task generates a report containing store performance metrics based on store activity and business hours data.

- Description: The task performs the following steps:
  1. Fetches store timezone, business hours, and store activity data from the database.
  2. Converts the fetched data into Pandas DataFrames for efficient processing.
  3. Initializes an empty list to store the metrics for each store.
  4. Iterates over each store's data to calculate metrics:
     - Filters activity data for the current store_id.
     - Determines the store's timezone.
     - Calculates the current time in the local timezone.
     - Calculates time ranges for the last hour, last day, and last week.
     - Filters business hours data that falls within these time ranges.
     - Calculates the total duration of valid business hours and active time within each time range.
     - Calculates uptime (in minutes) and downtime (in minutes) for each time range.
  5. Handles cases where a 'store_id' does not exist in the data by continuing to the next store.
  6. Stores the calculated metrics in a list.
  7. Creates a Pandas DataFrame to store the results.
  8. Saves the DataFrame as a CSV file with a filename based on the 'report_id'.
  9. Opens and wraps the CSV file as a Django File object.
  10. Serializes and saves the File object as a report file using the 'ReportFileSerializer'.

## Usage

To use the Celery tasks in your Django project:

1. Configure Celery: Ensure that Celery is properly configured in your Django project. You may need to configure a message broker such as RabbitMQ or Redis.

2. Task Execution: You can execute the Celery tasks using the `apply_async` method provided by Celery. For example:

   ```python
   # Import the tasks
   from myapp.tasks import update_store_status

   # Execute the task asynchronously
   update_store_status.apply_async()
   ```

3. Monitoring: Monitor the progress and results of Celery tasks using Celery's monitoring tools, logs, and task result storage.

## Note

- The `report_id` parameter is used as a unique identifier for the generated report and in the filename when generating reports.

- Handle errors and exceptions appropriately to ensure robust task execution and data integrity.

This README provides an overview of the Celery tasks and their usage within the Django project. Be sure to adapt the tasks and configurations to your specific project requirements.