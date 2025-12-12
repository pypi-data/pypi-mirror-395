import dlt
import os, requests, json
from src.constants import API_URLS
from dotenv import load_dotenv
load_dotenv()

def fetch_module_fields(module):
    try:
        response = requests.get(
            f"{API_URLS["HUBSPOT_CRM_API_BASE_URL"]}/properties{module}",
            headers={
                "Authorization": f"Bearer {os.getenv('HUBSPOT_PRIVATE_APP_ACCESS_TOKEN')}"
            }
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        
        if not results:
            print(f"No fields found for module {module}.")
            return []
        
        print(f"Found {len(results)} fields for module {module}.")
        return [property["name"] for property in results if property.get("name")]
    except Exception as e:
        print(f"Error fetching fields for module {module}: {e}")
        return []

def format_module_fields(module):
    return ",".join(fetch_module_fields(module))

resources = {
    "owners": {
        "name": "owners",
        "endpoint": "/crm/v3/owners"
    },
    "deals": {
        "name": "deals",
        "endpoint": "/crm/v3/objects/deals/search"
    },
    "deals_contacts": {
        "name": "deals_contacts",
        "endpoint": "/crm/v4/associations/deal/contact/batch/read"
    },
    "deals_pipelines": {
        "name": "deals_pipelines",
        "endpoint": "/crm/v3/pipelines/deals"
    },
    "companies": {
        "name": "companies",
        "endpoint": "/crm/v3/objects/companies/search"
    },
    "contacts": {
        "name": "contacts",
        "endpoint": "/crm/v3/objects/contacts/search",
        "incremental_key": "lastmodifieddate"
    },
    "contacts_companies": {
        "name": "contacts_companies",
        "endpoint": "/crm/v4/associations/contact/company/batch/read"
    },
    "goal_targets": {
        "name": "goal_targets",
        "endpoint": "/crm/v3/objects/goal_targets/search"
    },
    "leads": {
        "name": "leads",
        "endpoint": "/crm/v3/objects/leads/search"
    },
    "quotes": {
        "name": "quotes",
        "endpoint": "/crm/v3/objects/quotes/search"
    },
    "tickets": {
        "name": "tickets",
        "endpoint": "/crm/v3/objects/tickets/search"
    },
    "feedback_submissions": {
        "name": "feedback_submissions",
        "endpoint": "/crm/v3/objects/feedback_submissions/search"
    }
}

state = {
    "incremental_records_limit": 10000,
    "has_incremental_limit_reached": False
}

def fetch_module_data(module, params=None):

    try:

        data = []
        has_more_records = True
        next_page_cursor = None

        while has_more_records:

            if not params and params != {}:
                params = {
                    "limit": 100,
                    "properties": format_module_fields(f"/{module['endpoint'].rstrip('/').split('/')[-1]}")
                }
            
            if next_page_cursor:
                params[module.get("pagination_param", "after")] = next_page_cursor

            response = requests.get(
                f"{API_URLS["HUBSPOT_API_BASE_URL"]}{module['endpoint']}",
                headers={
                    "Authorization": f"Bearer {os.getenv('HUBSPOT_PRIVATE_APP_ACCESS_TOKEN')}"
                },
                params=params
            )

            response.raise_for_status()
            data.extend(response.json().get("results", []))

            if module.get("pagination_param"):
                next_page_cursor = response.json().get(module["pagination_param"])
                has_more_records = True if next_page_cursor else False
            else:
                next_page_cursor = response.json().get("paging", {}).get("next", {}).get("after")
                has_more_records = True if next_page_cursor else False

            print(f"Found {len(data)} records for module {module['endpoint']}.")

        for record in data:
            for key, value in record.items():
                if isinstance(value, list):
                    record[key] = json.dumps(value)

        resources[module['name']]['fetched_records'] = resources[module['name']].get("fetched_records", 0) + len(data)
        return data
        
    except Exception as e:
        print(f"Error fetching data for module {module['endpoint']}: {e}")

def fetch_module_incremental_data(module, incremental_value=None, payload=None):

    print(f"Fetching data for module {module['endpoint']} updated since {incremental_value}")

    try:

        data = []
        has_more_records = True
        next_page_cursor = None
        resources[module['name']]['fetched_records'] = 0

        while has_more_records and module.get("fetched_records", 200) < 10000:

            if not payload and payload != {}:
                payload = {
                    "filterGroups": [
                        {
                            "filters": [
                                {
                                    "propertyName": module.get("incremental_key", "hs_lastmodifieddate"),
                                    "operator": "GT",
                                    "value": incremental_value
                                }
                            ]
                        }
                    ],
                    "properties": fetch_module_fields(f"/{module['endpoint'].strip('/').split('/')[3]}"),
                    "limit": 200
                }
            
            if next_page_cursor:
                payload[module.get("pagination_param", "after")] = next_page_cursor

            response = requests.post(
                f"{API_URLS["HUBSPOT_API_BASE_URL"]}{module['endpoint']}",
                headers={
                    "Authorization": f"Bearer {os.getenv('HUBSPOT_PRIVATE_APP_ACCESS_TOKEN')}"
                },
                json=payload
            )

            response.raise_for_status()
            data.extend(response.json().get("results", []))
            
            if module.get("pagination_param"):
                next_page_cursor = response.json().get(module["pagination_param"])
                has_more_records = True if next_page_cursor else False
            else:
                next_page_cursor = response.json().get("paging", {}).get("next", {}).get("after")
                has_more_records = True if next_page_cursor else False

            total_records_fetched = len(data) or 0
            resources[module['name']]['fetched_records'] = total_records_fetched
            if(total_records_fetched >= 10000):
                state["has_incremental_limit_reached"] = True
            print(f"Found {total_records_fetched} records for module {module['endpoint']}.")

        for record in data:
            for key, value in record.items():
                if isinstance(value, list):
                    record[key] = json.dumps(value)
        return data
        
    except Exception as e:
        print(f"Error fetching data for module {module['endpoint']}: {e}")

@dlt.resource(name='owners', write_disposition='merge', max_table_nesting=1, primary_key='id')
def owners():
    params = {
        "limit": 500
    }
    yield fetch_module_data(resources["owners"], params)

@dlt.resource(name='deals', write_disposition='merge', max_table_nesting=1, primary_key='id')
def deals(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["deals"], updated_at.start_value)

@dlt.transformer(data_from=deals, name='deals_contacts', write_disposition='merge', max_table_nesting=1, primary_key='from__id')
def deals_contacts(deals):
    deal_ids = []
    for deal in deals:
        deal_ids.append(deal.get('id', None))
    yield fetch_resource_associated_data(resources["deals_contacts"], deal_ids)

@dlt.resource(name='deals_pipelines', write_disposition='merge', max_table_nesting=1, primary_key='id')
def deals_pipelines():
    params = {}
    yield fetch_module_data(resources["deals_pipelines"], params)

@dlt.resource(name='companies', write_disposition='merge', max_table_nesting=1, primary_key='id')
def companies(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["companies"], updated_at.start_value)

@dlt.resource(name='contacts', write_disposition='merge', max_table_nesting=1, primary_key='id')
def contacts(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["contacts"], updated_at.start_value)

@dlt.transformer(data_from=contacts, name='contacts_companies', write_disposition='merge', max_table_nesting=1, primary_key='from__id')
def contacts_companies(contacts):
    contact_ids = []
    for contact in contacts:
        contact_ids.append(contact.get('id', None))
    yield fetch_resource_associated_data(resources["contacts_companies"], contact_ids)

@dlt.resource(name='goal_targets', write_disposition='merge', max_table_nesting=1, primary_key='id')
def goal_targets(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["goal_targets"], updated_at.start_value)

@dlt.resource(name='leads', write_disposition='merge', max_table_nesting=1, primary_key='id')
def leads(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["leads"], updated_at.start_value)

@dlt.resource(name='quotes', write_disposition='merge', max_table_nesting=1, primary_key='id')
def quotes(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["quotes"], updated_at.start_value)

@dlt.resource(name='tickets', write_disposition='merge', max_table_nesting=1, primary_key='id')
def tickets(updated_at=dlt.sources.incremental("updatedAt")):
    yield fetch_module_incremental_data(resources["tickets"], updated_at.start_value)

def fetch_resource_associated_data(module, deal_ids):
    data = []
    batch_size = 1000
    for i in range(0, len(deal_ids), batch_size):
        ids_batch = deal_ids[i:i + batch_size]
        payload = {
            "inputs": [{"id": str(deal_id)} for deal_id in ids_batch]
        }
        data.extend(fetch_module_incremental_data(module, None, payload))
    return data

@dlt.source
def hubspot_historical_source():
    return [
        owners, 
        # companies, 
        # deals, deals_contacts, deals_pipelines,
        # contacts, contacts_companies, 
        # goal_targets, leads, quotes, tickets
    ]

def pipeline_hubspot() -> None:

    while not state["has_incremental_limit_reached"]:

        pipeline = dlt.pipeline(
            pipeline_name="hubspot_raw_pipeline",
            destination='bigquery',
            dataset_name="hubspot_raw",
            progress="log"
        )

        load_info = pipeline.run(hubspot_historical_source())
        print(load_info)

        if state["has_incremental_limit_reached"]:
            print(f"has_incremental_limit_reached 1", state["has_incremental_limit_reached"])
            state["has_incremental_limit_reached"] = False
        else:
            state["has_incremental_limit_reached"] = True

if __name__ == "__main__":
    pipeline_hubspot()