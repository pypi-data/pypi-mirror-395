from typing import Any, Dict, List, NamedTuple
import logging
import time
import datetime
import aiobotocore.session
from boto3.dynamodb.types import TypeDeserializer
import newrelic.agent
import asyncio


logger = logging.getLogger(__name__)


class FloatDeserializer(TypeDeserializer):
    def _deserialize_n(self, value):
        return float(value)


_deser = FloatDeserializer()


class FeatureRetrievalMeta(NamedTuple):
    cache_misses: int
    retrieval_ms: float
    success: bool
    cache_delay_minutes: float
    dynamo_ms: float
    parsing_ms: float


@newrelic.agent.function_trace()
async def async_batch_get(
    dynamo_client, table_name: str, keys: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Asynchronous batch_get_item with chunking for requests > 100 keys
    and handling for unprocessed keys.
    """
    # DynamoDB's BatchGetItem has a 100-item limit per request.
    CHUNK_SIZE = 100
    chunks = [keys[i : i + CHUNK_SIZE] for i in range(0, len(keys), CHUNK_SIZE)]
    tasks = [_fetch_chunk(dynamo_client, table_name, chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    all_items = [item for batch in results for item in batch]
    return all_items


async def _fetch_chunk(dynamo_client, table_name: str, chunk_keys):
    """Fetch a single chunk of up to 100 keys with retry handling."""
    to_fetch = {table_name: {"Keys": chunk_keys}}
    retries = 3
    items = []

    while to_fetch and retries > 0:
        retries -= 1
        try:
            resp = await dynamo_client.batch_get_item(RequestItems=to_fetch)

            # Collect retrieved items
            if "Responses" in resp and table_name in resp["Responses"]:
                items.extend(resp["Responses"][table_name])

            # Check for unprocessed keys
            unprocessed = resp.get("UnprocessedKeys", {})
            if unprocessed and unprocessed.get(table_name):
                unp = unprocessed[table_name]["Keys"]
                logger.warning("Retrying %d unprocessed keys.", len(unp))
                to_fetch = {table_name: {"Keys": unp}}
            else:
                to_fetch = {}

        except Exception as e:
            logger.error("Error in batch_get_item chunk: %s", e)
            break

    return items


@newrelic.agent.function_trace()
def parse_dynamo_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a DynamoDB attribute map (low-level) to Python types."""
    # out: Dict[str, Any] = {}
    return {k: _deser.deserialize(v) for k, v in item.items()}


@newrelic.agent.function_trace()
async def set_stream_features(
    *,
    streams: List[Dict[str, Any]],
    stream_features: List[str],
    features_cache,
    features_table: str,
    stream_pk_prefix: str,
    cache_sep: str,
    aio_session: aiobotocore.session.Session | None = None,
) -> FeatureRetrievalMeta:
    time_start = time.perf_counter_ns()
    """Fetch missing features for streams from DynamoDB and fill them into streams."""
    if not streams or not stream_features:
        return FeatureRetrievalMeta(
            cache_misses=0,
            retrieval_ms=(time.perf_counter_ns() - time_start) * 1e-6,
            success=True,
            cache_delay_minutes=0,
            dynamo_ms=0,
            parsing_ms=0,
        )

    cache_miss: Dict[str, Dict[str, Any]] = {}
    cache_delay_obj: dict[str, float] = {f: 0 for f in stream_features}
    now = datetime.datetime.utcnow()
    for f in stream_features:
        for s in streams:
            key = f"{s['streamUrl']}{cache_sep}{f}"
            if key in features_cache:
                # Only set if value is not None
                cached = features_cache.get(key)
                if cached["value"] is not None:
                    s[f] = cached["value"]
                    cache_delay_obj[f] = max(
                        cache_delay_obj[f],
                        (now - cached["inserted_at"]).total_seconds(),
                    )
            else:
                cache_miss[key] = s
    valid_cache_delays = list(v for v in cache_delay_obj.values() if v > 0)
    cache_delay = min(valid_cache_delays) if valid_cache_delays else 0

    if not cache_miss:
        return FeatureRetrievalMeta(
            cache_misses=0,
            retrieval_ms=(time.perf_counter_ns() - time_start) * 1e-6,
            success=True,
            cache_delay_minutes=cache_delay / 60,
            dynamo_ms=0,
            parsing_ms=0,
        )
    cache_misses = len(cache_miss)
    logger.info("Cache miss for %d items", cache_misses)

    # Prepare keys
    keys = []
    for k in cache_miss.keys():
        stream_url, sk = k.split(cache_sep, 1)
        pk = f"{stream_pk_prefix}{stream_url}"
        keys.append({"pk": {"S": pk}, "sk": {"S": sk}})

    session = aio_session or aiobotocore.session.get_session()
    dynamo_start = time.perf_counter_ns()
    async with session.create_client("dynamodb") as dynamodb:
        try:
            items = await async_batch_get(dynamodb, features_table, keys)
        except Exception as e:
            logger.error("DynamoDB batch_get failed: %s", e)
            end_time = time.perf_counter_ns()
            return FeatureRetrievalMeta(
                cache_misses=cache_misses,
                retrieval_ms=(end_time - time_start) * 1e-6,
                success=False,
                cache_delay_minutes=cache_delay / 60,
                dynamo_ms=(end_time - dynamo_start) * 1e-6,
                parsing_ms=0,
            )
    dynamo_end = time.perf_counter_ns()
    updated_keys = set()
    for item in items:
        stream_url = item["pk"]["S"].removeprefix(stream_pk_prefix)
        feature_name = item["sk"]["S"]
        cache_key = f"{stream_url}{cache_sep}{feature_name}"
        parsed = parse_dynamo_item(item)

        features_cache[cache_key] = {
            "value": parsed.get("value"),
            "cache_ttl_in_seconds": int(parsed.get("cache_ttl_in_seconds", -1)),
            "inserted_at": datetime.datetime.utcnow(),
        }
        if cache_key in cache_miss:
            cache_miss[cache_key][feature_name] = parsed.get("value")
            updated_keys.add(cache_key)
    parsing_end = time.perf_counter_ns()
    # Save keys that were not found in DynamoDB with None value
    if len(updated_keys) < len(cache_miss):
        missing_keys = set(cache_miss.keys()) - updated_keys
        for k in missing_keys:
            features_cache[k] = {"value": None, "cache_ttl_in_seconds": 300}
    end_time = time.perf_counter_ns()
    return FeatureRetrievalMeta(
        cache_misses=cache_misses,
        retrieval_ms=(end_time - time_start) * 1e-6,
        success=True,
        cache_delay_minutes=cache_delay / 60,
        dynamo_ms=(dynamo_end - dynamo_start) * 1e-6,
        parsing_ms=(parsing_end - dynamo_end) * 1e-6,
    )
