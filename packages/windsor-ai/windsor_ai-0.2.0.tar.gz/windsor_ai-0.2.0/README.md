# Windsor.ai Python SDK

A powerful, lightweight Python client and command-line interface (CLI) for the [Windsor.ai](https://windsor.ai/) API.

Easily fetch marketing data from Facebook, Google Ads, LinkedIn, and dozens of other platforms, unify it, and stream it directly into your Python scripts or data pipelines.

## Features

*   **Easy-to-use Client:** Simple Python wrapper for API endpoints.
*   **Built-in CLI:** Query data directly from your terminal—perfect for cron jobs or quick checks.
*   **Smart Filtering:** Helper classes to construct complex API filters easily.
*   **Data Streaming:** Efficiently handle massive datasets with pagination automagically handled via generators.
*   **Type Hints:** Fully typed for better developer experience in modern IDEs.

## Installation

Install the package via pip:

```bash
pip install windsor-ai
```

## Authentication

You need a Windsor.ai API key. You can pass it explicitly to the client or set it as an environment variable (recommended).

**Environment Variable:**
```bash
export WINDSOR_API_KEY="your_api_key_here"
```

## Python Library Usage

### 1. Basic Data Fetching

```python
from windsor_ai import Client

# Initialize (automatically reads WINDSOR_API_KEY env var)
client = Client(api_key="your_api_key") 

# Fetch data
response = client.connectors(
    connector="facebook",
    date_preset="last_7d",
    fields=["date", "campaign", "clicks", "spend", "impressions"]
)

for row in response['data']:
    print(f"{row['date']}: {row['campaign']} - ${row['spend']}")
```

### 2. Advanced Filtering

Use the `Filter` class to create readable, robust queries.

```python
from windsor_ai import Client, Filter

client = Client("your_api_key")

# Define filters
filters = [
    Filter("clicks", "gt", 100),            # Clicks greater than 100
    Filter("campaign", "contains", "Q4"),   # Campaign name contains "Q4"
]

data = client.connectors(
    connector="google_ads",
    date_preset="last_30d",
    fields=["campaign", "clicks", "cpc"],
    filters=filters
)
```

### 3. Handling Large Datasets (Streaming)

If you are exporting millions of rows, use `stream_connectors`. It yields records one by one, handling pagination behind the scenes so you don't run out of RAM.

```python
client = Client("your_api_key")

# Returns a generator, not a list
iterator = client.stream_connectors(
    connector="all",
    date_preset="last_year",
    fields=["source", "campaign", "clicks", "spend"]
)

for row in iterator:
    # Process row immediately (e.g., write to CSV or Database)
    save_to_db(row)
```

---

## CLI Usage

This package installs a command-line tool named `windsor`.

### 1. List Available Connectors

```bash
windsor list-connectors
```

### 2. Check Available Fields

See which metrics and dimensions are available for a specific platform.

```bash
windsor fields facebook
```

### 3. Query Data

Fetch data and output as JSON (default) or CSV.

```bash
# Fetch last 7 days of Facebook data
windsor query \
  --connector facebook \
  --date-preset last_7d \
  --fields date,campaign,clicks,spend \
  --format json
```

### 4. CLI Filtering and Exporting

You can filter data using the `field:operator:value` syntax.

**Operators:** `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `contains`, `ncontains`, `null`, `notnull`.

```bash
# Export Google Ads data to a CSV file
windsor query \
  --connector google_ads \
  --date-preset last_30d \
  --fields campaign,clicks,impressions \
  --filter "clicks:gt:50" \
  --filter "campaign:contains:Summer" \
  --format csv \
  --out report.csv
```

## Development

To contribute to this project:

1.  Clone the repository.
2.  Install dependencies and the package in editable mode:
    ```bash
    pip install -e .
    pip install build twine pytest flake8
    ```
3.  Run tests:
    ```bash
    # Requires WINDSOR_API_KEY to be set
    pytest
    ```

## License

This project is licensed under the MIT License.
