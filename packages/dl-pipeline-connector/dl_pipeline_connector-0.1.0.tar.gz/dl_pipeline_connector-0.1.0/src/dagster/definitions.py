from dagster import Definitions, load_assets_from_modules
from dagster_embedded_elt.dlt import DagsterDltResource
from src.dagster import assets
from .jobs import (
    hubspot_etl_operation_job,
)
from .schedulers import (
    hubspot_operation_job_scheduler,
)

all_assets = load_assets_from_modules([assets])
all_jobs = [
    hubspot_etl_operation_job,
]
all_schedulers = [
    hubspot_operation_job_scheduler,
]
dlt_resource = DagsterDltResource()

defs = Definitions(
    assets=all_assets,
    resources={"dlt": dlt_resource},
    jobs=all_jobs,
    schedules=all_schedulers
)