from dagster import job
from .assets import hubspot_etl_operation

@job()
def hubspot_etl_operation_job():
    hubspot_etl_operation()