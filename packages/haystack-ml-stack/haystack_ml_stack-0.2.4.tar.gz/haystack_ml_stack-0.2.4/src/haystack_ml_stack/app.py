import logging
import os
import random
import sys
from http import HTTPStatus
from typing import Any, Dict, List, Optional
import time

import aiobotocore.session
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
import newrelic.agent


from .cache import make_features_cache
from .dynamo import set_stream_features, FeatureRetrievalMeta
from .model_store import download_and_load_model
from .settings import Settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] [%(process)d] %(name)s : %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

logger = logging.getLogger(__name__)
APP_NAME = os.environ.get("NEW_RELIC_APP_NAME", None)


def create_app(
    settings: Optional[Settings] = None,
    *,
    preloaded_model: Optional[Dict[str, Any]] = None,
) -> FastAPI:
    """
    Build a FastAPI app with injectable settings and model.
    If `preloaded_model` is None, the app will load from S3 on startup.
    """
    cfg = settings or Settings()

    app = FastAPI(
        title="ML Stream Scorer",
        description="Scores video streams using a pre-trained ML model and DynamoDB features.",
        version="1.0.0",
    )

    # Mutable state: cache + model
    features_cache = make_features_cache(cfg.cache_maxsize)
    state: Dict[str, Any] = {
        "model": preloaded_model,
        "session": aiobotocore.session.get_session(),
        "model_name": (
            os.path.basename(cfg.s3_model_path) if cfg.s3_model_path else None
        ),
    }

    @app.on_event("startup")
    async def _startup() -> None:
        if state["model"] is not None:
            logger.info("Using preloaded model.")
            return

        if not cfg.s3_model_path:
            logger.critical("S3_MODEL_PATH not set; service will be unhealthy.")
            return

        try:
            state["model"] = await download_and_load_model(
                cfg.s3_model_path, aio_session=state["session"]
            )
            state["stream_features"] = state["model"].get("stream_features", [])
            logger.info("Model loaded on startup.")
        except Exception as e:
            logger.critical("Failed to load model: %s", e)

    @app.get("/health", status_code=HTTPStatus.OK)
    async def health():
        model_ok = state["model"] is not None
        if not model_ok:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="ML Model not loaded",
            )
        return {
            "status": "ok",
            "model_loaded": True,
            "cache_size": len(features_cache),
            "model_name": state.get("model_name"),
            "stream_features": state.get("stream_features", []),
        }

    @app.post("/score", status_code=HTTPStatus.OK)
    async def score_stream(request: Request, response: Response):
        if state["model"] is None:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="ML Model not loaded",
            )

        try:
            data = await request.json()
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid JSON payload"
            ) from e
        query_params = {}
        for k in request.query_params.keys():
            values = request.query_params.getlist(k)
            # flatten single-element lists
            query_params[k] = values[0] if len(values) == 1 else values
        user = data.get("user", {})
        streams: List[Dict[str, Any]] = data.get("streams", [])
        playlist = data.get("playlist", {})

        if not streams:
            logger.warning("No streams provided for user %s", user.get("userid", ""))
            return {}

        # Feature fetch (optional based on model)
        model = state["model"]
        stream_features = model.get("stream_features", []) or []
        retrieval_meta = FeatureRetrievalMeta(
            cache_misses=0,
            retrieval_ms=0,
            success=True,
            cache_delay_minutes=0,
            dynamo_ms=0,
            parsing_ms=0,
        )
        if stream_features:
            retrieval_meta = await set_stream_features(
                aio_session=state["session"],
                streams=streams,
                stream_features=stream_features,
                features_cache=features_cache,
                features_table=cfg.features_table,
                stream_pk_prefix=cfg.stream_pk_prefix,
                cache_sep=cfg.cache_separator,
            )

        random_number = random.random()
        userid = user.get("userid", "")
        # Sampling logs
        if random_number < cfg.logs_fraction:
            logger.info("User %s streams: %s", user.get("userid", ""), streams)

        # Synchronous model execution (user code)
        try:
            preprocess_start = time.perf_counter_ns()
            model["params"]["query_params"] = query_params
            model_input = model["preprocess"](
                user,
                streams,
                playlist,
                model["params"],
            )
            predict_start = time.perf_counter_ns()
            model_output = model["predict"](model_input, model["params"])
            predict_end = time.perf_counter_ns()
        except Exception as e:
            logger.error("Model prediction failed: %s", e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Model prediction failed",
            ) from e

        newrelic.agent.record_custom_event(
            "Inference",
            {
                "app_name": APP_NAME,
                "cache_misses": retrieval_meta.cache_misses,
                "retrieval_success": int(retrieval_meta.success),
                "cache_delay_minutes": retrieval_meta.cache_delay_minutes,
                "dynamo_ms": retrieval_meta.dynamo_ms,
                "dynamo_parse_ms": retrieval_meta.parsing_ms,
                "retrieval_ms": retrieval_meta.retrieval_ms,
                "preprocess_ms": (predict_start - preprocess_start) * 1e-6,
                "predict_ms": (predict_end - predict_start) * 1e-6,
                "total_streams": len(model_output),
            },
        )
        if model_output:
            if random_number < cfg.logs_fraction:
                logger.info(
                    "User %s - model output %s",
                    userid,
                    model_output,
                )
            return jsonable_encoder(model_output)

        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="No model output generated"
        )

    @app.get("/", status_code=HTTPStatus.OK)
    async def root():
        return {
            "message": "ML Scoring Service is running.",
            "model_name": state.get("model_name"),
        }

    return app
