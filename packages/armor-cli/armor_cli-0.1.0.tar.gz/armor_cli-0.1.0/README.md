# armor

Official Python SDK and CLI for [AnomalyArmor](https://anomalyarmor.ai) - Data Observability Platform.

## Installation

```bash
pip install armor
```

## Quick Start

```python
from armor import Client

# Initialize client (uses ARMOR_API_KEY env var)
client = Client()

# Check if data is fresh - raises StalenessError if stale
client.freshness.require_fresh("snowflake.prod.warehouse.orders")
print("Data is fresh, proceeding with pipeline...")
```

## Key Features

### Gate Pattern for Pipelines

The `require_fresh()` method fails fast if data is stale:

```python
from armor import Client
from armor.exceptions import StalenessError

client = Client()

try:
    client.freshness.require_fresh("snowflake.prod.warehouse.orders")
    # Data is fresh, safe to proceed
    run_transformation()
except StalenessError as e:
    # Data is stale, handle appropriately
    print(f"Stale: {e.asset} - last updated {e.last_updated}")
    # Fail the pipeline, send alert, etc.
```

### CLI for CI/CD

```bash
# Check freshness (exit 0=fresh, 1=stale)
armor freshness check snowflake.prod.warehouse.orders

# Use in CI/CD
armor freshness check snowflake.prod.warehouse.orders || exit 1
```

### Comprehensive Monitoring

```python
from armor import Client

client = Client()

# List assets
for asset in client.assets.list(source="snowflake"):
    print(f"{asset.qualified_name}: {asset.asset_type}")

# Check freshness status
status = client.freshness.get("snowflake.prod.warehouse.orders")
print(f"Fresh: {status.is_fresh}, Last updated: {status.last_updated}")

# Get lineage
lineage = client.lineage.get("snowflake.prod.warehouse.orders")
for upstream in lineage.upstream:
    print(f"Depends on: {upstream.qualified_name}")

# View alerts
alerts = client.alerts.list(status="triggered")
for alert in alerts:
    print(f"{alert.qualified_name}: {alert.message}")
```

## Configuration

Configuration can be set via:

1. **Environment variables** (highest priority)
   - `ARMOR_API_KEY`: Your API key
   - `ARMOR_API_URL`: API base URL

2. **Config file** (`~/.armor/config.yaml`)
   ```yaml
   api_key: aa_live_...
   ```

3. **Parameters** when initializing the client
   ```python
   client = Client(api_key="aa_live_...")
   ```

## CLI Commands

### Authentication
```bash
armor auth login    # Authenticate with API key
armor auth status   # Check authentication status
armor auth logout   # Remove stored credentials
```

### Assets
```bash
armor assets list                    # List all assets
armor assets list --source postgresql # Filter by source
armor assets get <qualified_name>    # Get asset details
```

### Freshness
```bash
armor freshness summary              # Get freshness summary
armor freshness get <asset>          # Check asset freshness
armor freshness list --status stale  # List stale assets
```

### Schema
```bash
armor schema summary                 # Get changes summary
armor schema changes                 # List all changes
armor schema changes --unacknowledged # Only unacknowledged
```

### Alerts
```bash
armor alerts summary                 # Get alerts summary
armor alerts list                    # List all alerts
armor alerts list --severity critical # Filter by severity
```

### API Keys
```bash
armor api-keys list                  # List API keys
armor api-keys create --name "CI/CD" # Create new key
armor api-keys revoke <key_id>       # Revoke a key
```

### Lineage
```bash
armor lineage get <asset>            # Get asset lineage
armor lineage get <asset> --depth 2  # With depth
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Asset is stale (freshness check) |
| 2 | Authentication error |
| 3 | Resource not found |
| 4 | Rate limit exceeded |
| 5 | General error |

## Examples

### CI/CD Pipeline Integration

```yaml
# .github/workflows/data-quality.yml
- name: Check data freshness
  run: |
    pip install armor-cli
    armor freshness get production.analytics.orders
  env:
    ARMOR_API_KEY: ${{ secrets.ARMOR_API_KEY }}
```

### Airflow Operator

```python
from airflow.operators.python import PythonOperator
from armor import Client

def check_upstream_freshness(asset_name: str):
    client = Client()
    status = client.freshness.get(asset_name)
    if status.is_stale:
        raise Exception(f"Upstream {asset_name} is stale")

check_freshness = PythonOperator(
    task_id="check_freshness",
    python_callable=check_upstream_freshness,
    op_kwargs={"asset_name": "production.raw.events"},
)
```

## Development

```bash
# Clone the repo
git clone https://github.com/anomalyarmor/armor-cli

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

## License

MIT
