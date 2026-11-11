from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import logging

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}')
logger = logging.getLogger(__name__)

app = FastAPI(title="Order Service")

ORDERS_PROCESSED = Counter("orders_processed_total", "Total orders processed")

class Order(BaseModel):
    item_id: str
    quantity: int

@app.get("/healthz")
def liveness():
    return {"status": "alive"}

@app.get("/readyz")
def readiness():
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/orders", status_code=201)
def create_order(order: Order):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    ORDERS_PROCESSED.inc()
    logger.info(f"Processed order for {order.item_id} x{order.quantity}")
    return {"status": "created", "item_id": order.item_id, "quantity": order.quantity}