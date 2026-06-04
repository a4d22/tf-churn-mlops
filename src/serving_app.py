from fastapi import FastAPI
import tensorflow as tf
from src.train import build_model
import numpy as np
import redis
import os

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="mlops_logger")


app = FastAPI(title="TF CHurn Prediction API")

MODEL = None
REDIS_CLIENT = None


@app.on_event("startup")
def load_model():
    global MODEL, REDIS_CLIENT

    # in real system , we would load model weights here
    MODEL = build_model()

    # read redis connection config from the nevironment variables
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", 6379)

    try:
        REDIS_CLIENT = redis.Redis(
            host=redis_host, port=redis_port, decode_responses=True
        )
        print(f"Connected to Redis at {redis_host}:{redis_port}")
    except Exception as e:
        print(f"Redis connection failed: {e}")


@app.get("/health")
def health_check():
    return {"status": "healthy", "tensorflow_version": tf.__version__}


@app.post("/predict/{customer_id}")
def predict(customer_id: str, features: list[float]):

    global MODEL, REDIS_CLIENT

    if REDIS_CLIENT:
        cached_prediction = REDIS_CLIENT.get(customer_id)
        if cached_prediction:
            # Structured JSON Log for Cache Hit
            log_payload = {
                "event": "inference",
                "customer_id": customer_id,
                "source": "cache",
                "churn_probability": float(cached_prediction),
            }
            logger.info(json.dumps(log_payload))

            return {
                "customer_id": customer_id,
                "churn_probability": float(cached_prediction),
                "source": "cache",
            }

    # If Cache miss: Run throught th tf model
    input_tensor = np.array([features], dtype=np.float32)

    # run inference
    prediction = MODEL(input_tensor)

    probability = float(prediction.numpy()[0][0])

    # Save to Cache for 60 seconds to save server resources
    if REDIS_CLIENT:
        REDIS_CLIENT.setex(name=customer_id, time=60, value=str(probability))

    # Structured JSON Log for Model Inference (Vital for Drift Audit!)
    log_payload = {
        "event": "inference",
        "customer_id": customer_id,
        "source": "tensorflow_model",
        "input_features": features,
        "churn_probability": probability,
    }
    logger.info(json.dumps(log_payload))

    return {
        "churn_probability": probability,
        "action": "churn" if probability > 0.5 else "retain",
        "source": "tensorflow_model",
    }
