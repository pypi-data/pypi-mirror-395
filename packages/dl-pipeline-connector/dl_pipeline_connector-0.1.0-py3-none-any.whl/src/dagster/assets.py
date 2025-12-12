from dagster import op
from src.pipelines import pipeline_hubspot

@op
def hubspot_etl_operation():
    pipeline_hubspot()