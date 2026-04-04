from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Allow Cloud Run frontend to call this API.
# Set FRONTEND_ORIGIN to your deployed frontend URL.
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cakes")
def get_cakes():
    return [
        {"name": "Chocolate Cake", "price": 500},
        {"name": "Red Velvet", "price": 600},
    ]


class Order(BaseModel):
    item: str
    quantity: int


@app.post("/order")
def create_order(order: Order):
    return {
        "message": "Order placed successfully!!",
        "order": order.dict(),
    }
