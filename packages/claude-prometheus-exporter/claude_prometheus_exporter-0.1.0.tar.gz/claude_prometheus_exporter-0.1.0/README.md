# Claude Prometheus Exporter

A Prometheus exporter for Claude API usage and cost metrics.

## Features

- **Token Metrics**: Track input, output, cache read, and cache creation tokens
- **Request Metrics**: Monitor API request counts
- **Cost Metrics**: Track API costs in USD
- **Automatic Collection**: Continuous metric collection with configurable intervals
- **Simple**: Single-file implementation following the same pattern as updownio-exporter

## Prerequisites

- Python 3.13+
- Poetry (for dependency management)
- Claude Admin API key (starts with `sk-ant-admin...`)

## Installation

```bash
poetry install
```

## Configuration

Configuration via environment variables or config files:

### Environment Variables

```bash
export APIKEY="sk-ant-admin-..."
export PROMETHEUS_PORT=9001
export LOOP_INTERVAL=30
export LOGGING_LEVEL=INFO
```

### Config Files

Place a JSON config file at:
- `/etc/claude-prometheus/claude-prometheus.json`
- `~/.config/claude-prometheus.json`

Example config:
```json
{
  "apikey": "sk-ant-admin-...",
  "prometheus": {
    "port": 9001,
    "namespace": "claude"
  },
  "loop": {
    "interval": 30
  },
  "logging": {
    "level": "INFO"
  }
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `apikey` | Claude Admin API key | Required |
| `prometheus.port` | Port to expose metrics on | 9001 |
| `prometheus.namespace` | Prometheus namespace | claude |
| `loop.interval` | Seconds between collections | 30 |
| `logging.level` | Log level (DEBUG, INFO, WARNING, ERROR) | INFO |

**Note**: The exporter always fetches data from midnight (UTC) to now on each collection. It uses delta calculation to avoid double-counting, so counters only increment with new usage since the last collection.

## Usage

```bash
poetry run python claude_prometheus.py
```

Or with custom config:
```bash
export APIKEY="sk-ant-admin-..."
export LOOP_INTERVAL=60
poetry run python claude_prometheus.py
```

## Metrics Endpoint

Once running, metrics are available at:
```
http://localhost:9001/metrics
```

## Exported Metrics

All metrics use the `claude_` namespace prefix (configurable).

### Token Metrics

- `claude_tokens_total` (Counter): Total tokens consumed by type
  - Labels: `type` (input, output, cache_read, cache_creation), `model`, `api_key_id`, `api_key_name`, `owner_email`, `owner_name`
- `claude_tokens_current` (Gauge): Tokens in current period
  - Labels: `type`, `model`, `api_key_id`, `api_key_name`, `owner_email`, `owner_name`

### Request Metrics

- `claude_requests_total` (Counter): Total API requests
  - Labels: `model`, `api_key_id`, `api_key_name`, `owner_email`, `owner_name`
- `claude_requests_current` (Gauge): Requests in current period
  - Labels: `model`, `api_key_id`, `api_key_name`, `owner_email`, `owner_name`

### Cost Metrics

- `claude_cost_total_usd` (Counter): Total cumulative cost in USD
  - Labels: `workspace_id`
- `claude_cost_current_usd` (Gauge): Cost in current period in USD
  - Labels: `workspace_id`

### Daemon Metrics

Provided by `daemon-metrics`:
- `claude_prometheus_loop_duration_seconds`: Duration of each collection loop
- `claude_prometheus_loop_success`: Whether the last loop succeeded
- `claude_prometheus_item_success`: Per-API-key success metrics

## Getting an Admin API Key

1. Log in to the [Claude Console](https://console.anthropic.com/)
2. Navigate to the Admin settings (requires admin role)
3. Generate an Admin API key

**Note**: Standard API keys (starting with `sk-ant-api`) will NOT work.

## Example Prometheus Configuration

Add this to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'claude-exporter'
    scrape_interval: 60s
    static_configs:
      - targets: ['localhost:9001']
```

## Example Queries

### Total tokens by model
```promql
sum by (model) (rate(claude_tokens_total[5m]))
```

### Total tokens by API key owner
```promql
sum by (owner_name, owner_email) (rate(claude_tokens_total[5m]))
```

### Total tokens by API key
```promql
sum by (api_key_id, api_key_name) (rate(claude_tokens_total[5m]))
```

### Request rate by owner
```promql
sum by (owner_name) (rate(claude_requests_total[5m]))
```

### Top users by token usage
```promql
topk(10, sum by (owner_name, owner_email) (claude_tokens_current))
```

### Top API keys by usage
```promql
topk(10, sum by (api_key_name, owner_name) (claude_tokens_current))
```

### Current cost by workspace
```promql
sum by (workspace_id) (claude_cost_current_usd)
```

## Development

### Code Quality Tools

```bash
# Format code
poetry run black claude_prometheus.py

# Type checking
poetry run mypy claude_prometheus.py

# Linting
poetry run pylint claude_prometheus.py
poetry run flake8 claude_prometheus.py
poetry run pycodestyle claude_prometheus.py
```

## Architecture

Following the same pattern as `updownio-exporter`, this is a single-file implementation with:
- Configuration management via `the-conf`
- Daemon metrics via `daemon-metrics`
- Clean collection loop with proper timing
- Prometheus metrics via `prometheus_client`

## Troubleshooting

### Authentication Errors
Ensure you're using an Admin API key (starts with `sk-ant-admin`).

### Permission Errors
Your API key must have admin permissions to access usage/cost data.

### No Data in Metrics
- Check that your organization has recent API usage
- Adjust `loop.lookback` to a longer period
- Check logs for API errors

## License

MIT
