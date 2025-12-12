import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import daemon_metrics
import requests
from prometheus_client import Counter, Gauge, Info, start_http_server
from the_conf import TheConf

conf = TheConf(
    {
        "source_order": ["env", "files"],
        "config_files": [
            "/etc/claude-prometheus-exporter/claude-prometheus-exporter.json",
            "~/.config/claude-prometheus-exporter.json",
        ],
        "parameters": [
            {"name": {"default": "claude-prometheus-exporter"}},
            {"apikey": {"type": str}},
            {
                "loop": [
                    {"interval": {"default": 30, "help": "seconds"}},
                ]
            },
            {
                "prometheus": [
                    {"port": {"type": "int", "default": 9100}},
                    {"namespace": {"default": "claude"}},
                ]
            },
            {"loglevel": {"default": "WARNING"}},
        ],
    }
)

logger = logging.getLogger("claude-prometheus-exporter")
try:
    logger.setLevel(getattr(logging, conf.loglevel.upper()))
    logger.addHandler(logging.StreamHandler())
except AttributeError as error:
    raise AttributeError(
        f"{conf.loglevel} isn't accepted, only DEBUG, INFO, WARNING, "
        "ERROR and FATAL are accepted"
    ) from error


BASE_URL = "https://api.anthropic.com"
ANTHROPIC_VERSION = "2023-06-01"

# Global cache for API key metadata
api_key_metadata = (
    {}
)  # {api_key_id: {"name": str, "owner_email": str, "owner_name": str}}


# Cache for tracking previous values to calculate deltas
class MetricsCache:
    """Cache to store previous metric values for delta calculation."""

    def __init__(self):
        self.tokens = {}  # {(type, model, api_key_id): value}
        self.requests = {}  # {(model, api_key_id): value}
        self.cost = {}  # {workspace_id: value}

    def get_token_delta(self, token_type, model, api_key_id, new_value):
        """Get delta for token metric."""
        key = (token_type, model, api_key_id)
        old_value = self.tokens.get(key, 0)
        self.tokens[key] = new_value
        return max(0, new_value - old_value)

    def get_request_delta(self, model, api_key_id, new_value):
        """Get delta for request metric."""
        key = (model, api_key_id)
        old_value = self.requests.get(key, 0)
        self.requests[key] = new_value
        return max(0, new_value - old_value)

    def get_cost_delta(self, workspace_id, new_value):
        """Get delta for cost metric."""
        old_value = self.cost.get(workspace_id, 0.0)
        self.cost[workspace_id] = new_value
        return max(0.0, new_value - old_value)

    def reset(self):
        """Reset all cached values (called at midnight)."""
        self.tokens.clear()
        self.requests.clear()
        self.cost.clear()


cache = MetricsCache()

# Metrics definitions
claude_tokens = Counter(
    "tokens_total",
    "Total tokens consumed",
    [
        "type",
        "model",
        "api_key_id",
        "api_key_name",
        "owner_email",
        "owner_name",
    ],
    namespace=conf.prometheus.namespace,
)

claude_requests = Counter(
    "requests_total",
    "Total API requests",
    ["model", "api_key_id", "api_key_name", "owner_email", "owner_name"],
    namespace=conf.prometheus.namespace,
)

claude_cost = Counter(
    "cost_total_usd",
    "Total cost in USD",
    ["workspace_id"],
    namespace=conf.prometheus.namespace,
)

claude_tokens_current = Gauge(
    "tokens_current",
    "Tokens in current period",
    [
        "type",
        "model",
        "api_key_id",
        "api_key_name",
        "owner_email",
        "owner_name",
    ],
    namespace=conf.prometheus.namespace,
)

claude_requests_current = Gauge(
    "requests_current",
    "Requests in current period",
    ["model", "api_key_id", "api_key_name", "owner_email", "owner_name"],
    namespace=conf.prometheus.namespace,
)

claude_cost_current = Gauge(
    "cost_current_usd",
    "Cost in current period",
    ["workspace_id"],
    namespace=conf.prometheus.namespace,
)

claude_exporter_info = Info(
    "exporter",
    "Exporter information",
    namespace=conf.prometheus.namespace,
)


def get_organization_users(api_key: str) -> dict:
    """Fetch organization users to get email and name mapping."""
    url = f"{BASE_URL}/v1/organizations/users"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }

    users = {}
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        for user in data.get("data", []):
            user_id = user.get("id")
            users[user_id] = {
                "email": user.get("email", "unknown"),
                "name": user.get("name", "unknown"),
            }

        logger.info("Fetched %d organization users", len(users))
        return users
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch organization users: %s", e)
        return {}


def get_api_key_info(api_key: str, api_key_id: str) -> Optional[dict]:
    """Fetch API key metadata including creator information."""
    url = f"{BASE_URL}/v1/organizations/api_keys/{api_key_id}"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.debug("Failed to fetch API key %s info: %s", api_key_id, e)
        return None


def refresh_api_key_metadata(admin_api_key: str, api_key_ids: set):
    """Refresh metadata for API keys by fetching user info and key details.

    Args:
        admin_api_key: Admin API key for authentication
        api_key_ids: Set of API key IDs to fetch metadata for
    """
    # Fetch all organization users
    users = get_organization_users(admin_api_key)

    # Fetch metadata for each API key
    for api_key_id in api_key_ids:
        if api_key_id in api_key_metadata:
            continue  # Already cached

        key_info = get_api_key_info(admin_api_key, api_key_id)
        if not key_info:
            # Set defaults if we can't fetch
            api_key_metadata[api_key_id] = {
                "name": "unknown",
                "owner_email": "unknown",
                "owner_name": "unknown",
            }
            continue

        key_name = key_info.get("name", "unknown")
        created_by = key_info.get("created_by", {})
        creator_id = created_by.get("id", "unknown")

        # Look up creator in users
        creator = users.get(creator_id, {})
        owner_email = creator.get("email", "unknown")
        owner_name = creator.get("name", "unknown")

        api_key_metadata[api_key_id] = {
            "name": key_name,
            "owner_email": owner_email,
            "owner_name": owner_name,
        }

        logger.debug(
            "API Key %s: name=%s, owner=%s (%s)",
            api_key_id,
            key_name,
            owner_name,
            owner_email,
        )

    logger.info("API key metadata cache has %d entries", len(api_key_metadata))


def get_usage_report(
    api_key: str, starting_at: str, ending_at: str
) -> Optional[dict]:
    """Fetch usage report from Claude API."""
    url = f"{BASE_URL}/v1/organizations/usage_report/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }
    params = {
        "starting_at": starting_at,
        "ending_at": ending_at,
        "bucket_width": "1h",
    }
    # Add multiple group_by parameters
    # Note: requests doesn't handle array params well, so we build manually
    group_by = ["model", "api_key_id"]
    param_list = []
    for key, value in params.items():
        param_list.append(f"{key}={value}")
    for group in group_by:
        param_list.append(f"group_by[]={group}")

    full_url = f"{url}?{'&'.join(param_list)}"

    logger.debug("Fetching usage report: %s to %s", starting_at, ending_at)
    try:
        response = requests.get(full_url, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch usage report: %s", e)
        return None


def get_cost_report(api_key: str) -> Optional[dict]:
    """Fetch cost report from Claude API.

    Note: Cost report only supports daily granularity, so we fetch
    the last 7 days of cost data.
    """
    url = f"{BASE_URL}/v1/organizations/cost_report"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }

    # Cost API requires date-only format and daily granularity
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=7)

    params = {
        "starting_at": start_date.isoformat(),
        "ending_at": end_date.isoformat(),
        "group_by[]": "workspace_id",
    }

    logger.debug("Fetching cost report: %s to %s", start_date, end_date)
    try:
        response = requests.get(
            url, headers=headers, params=params, timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch cost report: %s", e)
        return None


def process_usage_data(usage_data: dict):
    """Process usage data and update metrics.

    Since we fetch from midnight to now, we need to calculate deltas
    to avoid double-counting on each loop iteration.

    The API returns data in time buckets, each with a 'results' array.
    """
    buckets = usage_data.get("data", [])
    logger.info("Processing %d time buckets", len(buckets))

    total_items = 0
    for bucket in buckets:
        results = bucket.get("results", [])
        total_items += len(results)

        for item in results:
            model = item.get("model", "unknown")
            api_key_id = item.get("api_key_id", "unknown")

            # Get API key metadata
            metadata = api_key_metadata.get(
                api_key_id,
                {
                    "name": "unknown",
                    "owner_email": "unknown",
                    "owner_name": "unknown",
                },
            )
            api_key_name = metadata["name"]
            owner_email = metadata["owner_email"]
            owner_name = metadata["owner_name"]

            # Token fields in the API response
            uncached_input_tokens = item.get("uncached_input_tokens", 0)
            cache_read_tokens = item.get("cache_read_input_tokens", 0)
            output_tokens = item.get("output_tokens", 0)

            # Cache creation tokens (nested structure)
            cache_creation = item.get("cache_creation", {})
            cache_creation_1h = cache_creation.get(
                "ephemeral_1h_input_tokens", 0
            )
            cache_creation_5m = cache_creation.get(
                "ephemeral_5m_input_tokens", 0
            )
            cache_creation_tokens = cache_creation_1h + cache_creation_5m

            # Total input tokens
            input_tokens = uncached_input_tokens + cache_creation_tokens

            # Note: API doesn't provide num_requests, we'll estimate as 1
            # per result
            num_requests = 1

            logger.debug(
                "Raw values - Model: %s, API Key: %s, Input: %d, Output: %d",
                model,
                api_key_id,
                input_tokens,
                output_tokens,
            )

            # Calculate deltas and update counters
            for token_type, value in [
                ("input", input_tokens),
                ("output", output_tokens),
                ("cache_read", cache_read_tokens),
                ("cache_creation", cache_creation_tokens),
            ]:
                delta = cache.get_token_delta(
                    token_type, model, api_key_id, value
                )
                logger.debug(
                    "Token delta - Type: %s, Model: %s, API Key: %s, "
                    "Value: %d, Delta: %d",
                    token_type,
                    model,
                    api_key_id,
                    value,
                    delta,
                )
                if delta > 0:
                    logger.info(
                        "Incrementing counter: type=%s, model=%s, "
                        "api_key_id=%s by %d",
                        token_type,
                        model,
                        api_key_id,
                        delta,
                    )
                    claude_tokens.labels(
                        type=token_type,
                        model=model,
                        api_key_id=api_key_id,
                        api_key_name=api_key_name,
                        owner_email=owner_email,
                        owner_name=owner_name,
                    ).inc(delta)

            delta_requests = cache.get_request_delta(
                model, api_key_id, num_requests
            )
            logger.debug(
                "Request delta - Model: %s, API Key: %s, Value: %d, Delta: %d",
                model,
                api_key_id,
                num_requests,
                delta_requests,
            )
            if delta_requests > 0:
                logger.info(
                    "Incrementing requests counter: "
                    "model=%s, api_key_id=%s by %d",
                    model,
                    api_key_id,
                    delta_requests,
                )
                claude_requests.labels(
                    model=model,
                    api_key_id=api_key_id,
                    api_key_name=api_key_name,
                    owner_email=owner_email,
                    owner_name=owner_name,
                ).inc(delta_requests)

            # Update gauges
            claude_tokens_current.labels(
                type="input",
                model=model,
                api_key_id=api_key_id,
                api_key_name=api_key_name,
                owner_email=owner_email,
                owner_name=owner_name,
            ).set(input_tokens)
            claude_tokens_current.labels(
                type="output",
                model=model,
                api_key_id=api_key_id,
                api_key_name=api_key_name,
                owner_email=owner_email,
                owner_name=owner_name,
            ).set(output_tokens)
            claude_tokens_current.labels(
                type="cache_read",
                model=model,
                api_key_id=api_key_id,
                api_key_name=api_key_name,
                owner_email=owner_email,
                owner_name=owner_name,
            ).set(cache_read_tokens)
            claude_tokens_current.labels(
                type="cache_creation",
                model=model,
                api_key_id=api_key_id,
                api_key_name=api_key_name,
                owner_email=owner_email,
                owner_name=owner_name,
            ).set(cache_creation_tokens)
            claude_requests_current.labels(
                model=model,
                api_key_id=api_key_id,
                api_key_name=api_key_name,
                owner_email=owner_email,
                owner_name=owner_name,
            ).set(num_requests)

    logger.info(
        "Processed %d usage result items across all buckets", total_items
    )


def process_cost_data(cost_data: dict):
    """Process cost data and update metrics.

    Since we fetch from midnight to now, we need to calculate deltas
    to avoid double-counting on each loop iteration.

    The API returns data in time buckets, each with a 'results' array.
    """
    buckets = cost_data.get("data", [])
    logger.info("Processing %d cost time buckets", len(buckets))

    total_items = 0
    for bucket in buckets:
        results = bucket.get("results", [])
        total_items += len(results)

        for item in results:
            workspace_id = item.get("workspace_id")
            if workspace_id is None:
                workspace_id = "default"

            # Cost is in the 'amount' field as a string in USD
            amount_str = item.get("amount", "0")
            cost_usd = float(amount_str)

            logger.debug(
                "Raw cost - Workspace: %s, Amount: %s, Cost USD: %.2f",
                workspace_id,
                amount_str,
                cost_usd,
            )

            delta_cost = cache.get_cost_delta(workspace_id, cost_usd)
            logger.debug(
                "Cost delta - Workspace: %s, Value: %.2f, Delta: %.2f",
                workspace_id,
                cost_usd,
                delta_cost,
            )
            if delta_cost > 0:
                logger.info(
                    "Incrementing cost counter: workspace_id=%s by $%.2f",
                    workspace_id,
                    delta_cost,
                )
                claude_cost.labels(workspace_id=workspace_id).inc(delta_cost)

            claude_cost_current.labels(workspace_id=workspace_id).set(cost_usd)

    logger.info(
        "Processed %d cost result items across all buckets", total_items
    )


def collect_metrics(api_key: str) -> bool:
    """Collect all metrics from Claude API.

    Fetches data from midnight (UTC) to now to get the full day's usage.
    Uses delta calculation to avoid double-counting on each loop.
    """
    now = datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    starting_at = midnight.strftime("%Y-%m-%dT%H:%M:%SZ")
    ending_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    logger.debug(
        "Fetching metrics from %s to %s (since midnight)",
        starting_at,
        ending_at,
    )

    success = True

    # Fetch and process usage data
    usage_data = get_usage_report(api_key, starting_at, ending_at)
    logger.debug("Usage data response: %s", usage_data)
    if usage_data:
        # Extract API key IDs from usage data
        api_key_ids = set()
        for bucket in usage_data.get("data", []):
            for result in bucket.get("results", []):
                api_key_id = result.get("api_key_id")
                if api_key_id:
                    api_key_ids.add(api_key_id)

        # Refresh metadata for any new API keys
        if api_key_ids:
            logger.info(
                "Found %d unique API keys, refreshing metadata",
                len(api_key_ids),
            )
            refresh_api_key_metadata(api_key, api_key_ids)

        process_usage_data(usage_data)
    else:
        success = False
        logger.warning("No usage data received")

    # Fetch and process cost data
    cost_data = get_cost_report(api_key)
    logger.debug("Cost data response: %s", cost_data)
    if cost_data:
        process_cost_data(cost_data)
    else:
        success = False
        logger.warning("No cost data received")

    return success


def main():
    info = {
        "loop-period": conf.loop.interval,
    }
    daemon_metrics.init(conf.name, info)

    # Set exporter info
    claude_exporter_info.info(
        {
            "version": "0.1.0",
            "scrape_interval": str(conf.loop.interval),
            "collection_window": "midnight to now (UTC)",
        }
    )

    last_date = None

    while True:
        loop_context = daemon_metrics.LoopContext(conf.name)
        with loop_context:
            # Check if we crossed midnight and reset cache
            current_date = datetime.now(timezone.utc).date()
            if last_date is not None and current_date != last_date:
                logger.info("Midnight crossed, resetting metric cache")
                cache.reset()
            last_date = current_date

            try:
                success = collect_metrics(conf.apikey)
                daemon_metrics.item_result(conf.name, success, "claude_api")
            except Exception:
                logger.exception("Failed to collect metrics")
                daemon_metrics.item_result(conf.name, False, "claude_api")

        if (interval := conf.loop.interval - loop_context.exec_interval) > 0:
            time.sleep(interval)


if __name__ == "__main__":
    logger.info("Starting %s", conf.name)
    start_http_server(conf.prometheus.port)
    main()
