import dagster as dg
from .jobs import hubspot_etl_operation_job

hubspot_operation_job_scheduler = dg.ScheduleDefinition(
    job=hubspot_etl_operation_job,
    cron_schedule="0 */3 * * *",
    execution_timezone="Europe/Berlin",
    name="hubspot_operation_job_scheduler",
    default_status=dg.DefaultScheduleStatus.RUNNING
)