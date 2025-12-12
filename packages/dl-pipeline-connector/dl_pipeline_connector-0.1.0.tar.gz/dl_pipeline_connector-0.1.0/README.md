# DL Pipeline Connector

A data pipeline connector for ETL processes built with dlt (data load tool) and Dagster, focusing on extracting data from HubSpot CRM and loading it into BigQuery.

## Features

- HubSpot CRM data extraction with incremental loading
- BigQuery destination support
- Dagster orchestration integration
- Multiple HubSpot resources: contacts, companies, deals, engagement activities, and more
- Incremental data loading with state management
- Automated pipeline scheduling and monitoring

## Project Structure

```
dl-pipeline-connector/
├── src/
│   ├── pipelines/                 # ETL pipeline implementations
│   │   ├── hubspot.py            # HubSpot to BigQuery pipeline
│   │   └── __init__.py
│   ├── dagster/                   # Dagster orchestration
│   │   ├── assets.py             # Dagster assets definitions
│   │   ├── definitions.py        # Dagster definitions
│   │   ├── jobs.py               # Dagster jobs
│   │   ├── schedulers.py         # Dagster schedulers
│   │   ├── sensors.py            # Dagster sensors
│   │   └── __init__.py
│   ├── dagster_test/              # Dagster testing utilities
│   │   └── __init__.py
│   ├── constants/                 # Constants and configuration
│   │   └── urls.py               # API URLs
│   └── __init__.py
├── .github/                       # GitHub configuration
├── .venv/                         # Virtual environment
├── pyproject.toml                 # Project configuration & dependencies
├── .env.example                   # Environment variables template
├── .env                           # Environment variables (gitignored)
├── .gitignore                     # Git ignore rules
├── UV_GUIDE.md                    # UV package manager guide
└── README.md
```

## Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- HubSpot account with API access
- Google Cloud Platform account with BigQuery enabled

### Install uv

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Project Setup

1. Clone the repository and navigate to the project directory:
```bash
cd dl-pipeline-connector
```

2. Sync the project (creates venv and installs dependencies):
```bash
uv sync
```

3. Install the core dependencies:
```bash
uv add "dlt[bigquery]" dagster dagster-embedded-elt dagster-webserver dagster-slack
```

4. Install development dependencies:
```bash
uv add --dev pytest pytest-cov ruff mypy
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Required environment variables in `.env`:
- `HUBSPOT_PRIVATE_APP_ACCESS_TOKEN` - Your HubSpot private app access token
- `DESTINATION__BIGQUERY__LOCATION` - BigQuery dataset location (e.g., US, EU)
- `DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID` - GCP project ID
- `DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY` - GCP service account private key
- `DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL` - GCP service account email

## Usage

### Running the HubSpot Pipeline

Activate your virtual environment first:
```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

Run the HubSpot pipeline directly:
```bash
python -m pipelines.hubspot
```

Or import and run programmatically:
```python
from pipelines.hubspot import pipeline_hubspot

# Run the pipeline
pipeline_hubspot()
```

### Running with Dagster

Start the Dagster web server:
```bash
dagster dev
```

This will start the Dagster UI at http://localhost:3000 where you can:
- View pipeline definitions and assets
- Trigger manual runs
- Monitor pipeline execution
- View run history and logs
- Configure schedules and sensors

### Available HubSpot Resources

The pipeline extracts the following HubSpot resources:

**Core Objects:**
- `owners` - HubSpot users and owners
- `companies` - Company records (incremental)
- `contacts` - Contact records (incremental)
- `deals` - Deal records (incremental)
- `leads` - Lead records (incremental)
- `quotes` - Quote records (incremental)
- `tickets` - Ticket records (incremental)
- `goal_targets` - Goal target records (incremental)

**Pipelines:**
- `deals_pipelines` - Deal pipeline configurations

**Associations:**
- `deals_contacts` - Deal-to-contact associations
- `contacts_companies` - Contact-to-company associations

**Engagement Activities:**
- `engagement_calls` - Call activities (incremental)
- `engagement_communications` - Communication activities (incremental)
- `engagement_meetings` - Meeting activities (incremental)
- `engagement_notes` - Note activities (incremental)
- `engagement_tasks` - Task activities (incremental)

## Pipeline Configuration

### Incremental Loading

The pipeline uses dlt's incremental loading feature to only fetch records that have been updated since the last run. The state is automatically managed by dlt.

**Incremental Key:** Most resources use `updatedAt` as the incremental cursor field.

**Batch Limits:** The pipeline fetches up to 10,000 records per incremental run to avoid API rate limits and timeouts. If more records exist, the pipeline will run multiple times until all data is synchronized.

### Write Disposition

All resources use `write_disposition='merge'` which means:
- New records are inserted
- Existing records (based on primary key) are updated
- No data is deleted from the destination

### BigQuery Dataset

Data is loaded into the `hubspot_raw` dataset in BigQuery. Each resource becomes a separate table.

## Managing Dependencies

### Current Dependencies

**Core ETL:**
- `dlt[bigquery]` - Data load tool with BigQuery support
- `dagster` - Orchestration framework
- `dagster-embedded-elt` - Embedded ELT capabilities
- `dagster-webserver` - Web UI for Dagster
- `dagster-slack` - Slack notifications

**Development:**
- `pytest` - Testing framework
- `pytest-cov` - Test coverage
- `ruff` - Python linter and formatter
- `mypy` - Static type checking

### Adding New Dependencies

Use `uv add` to automatically install and update `pyproject.toml`:

```bash
# Add a production dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Add a specific version
uv add <package-name>==1.2.3

# Add with extras
uv add "package[extra1,extra2]"
```

No manual `pyproject.toml` editing needed - `uv add` handles it automatically!

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## Code Quality

The project uses modern Python tooling for code quality:

```bash
# Format code with ruff
ruff format .

# Lint and auto-fix issues
ruff check . --fix

# Type checking with mypy
mypy src/

# Run all quality checks
ruff check . && ruff format --check . && mypy src/
```

### Ruff Configuration

Configured in [pyproject.toml](pyproject.toml):
- Line length: 100 characters
- Target: Python 3.10+
- Selected rules: Errors (E), Pyflakes (F), Import sorting (I), Naming (N), Warnings (W), Pyupgrade (UP)

## Development Workflow

1. Create a new branch for your feature/fix
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes to the codebase

3. Add tests for new functionality in `tests/`

4. Run code quality checks:
```bash
ruff check . --fix
ruff format .
mypy src/
pytest
```

5. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

6. Push and create a pull request
```bash
git push origin feature/your-feature-name
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'pipelines'**
- Make sure you're in the project root directory
- Activate your virtual environment
- Run with `python -m pipelines.hubspot` instead of direct execution

**BigQuery Authentication Error**
- Verify your service account credentials in `.env`
- Ensure the private key is properly formatted with `\n` for line breaks
- Check that the service account has BigQuery Data Editor and Job User roles

**HubSpot API Rate Limits**
- The pipeline implements pagination and batch limits
- Rate limit errors are logged - wait and retry
- Consider adjusting batch sizes in [hubspot.py](src/pipelines/hubspot.py)

**dlt State Issues**
- Pipeline state is stored in `.dlt/` directory
- To reset incremental state, delete `.dlt/` and run full refresh
- State is also persisted in BigQuery in `_dlt_loads` and `_dlt_pipeline_state` tables

## Project Links

- [dlt Documentation](https://dlthub.com/docs)
- [Dagster Documentation](https://docs.dagster.io)
- [HubSpot API Reference](https://developers.hubspot.com/docs/api/overview)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [uv Package Manager](https://github.com/astral-sh/uv)

## License

[Your License Here]
