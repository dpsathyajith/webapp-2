from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

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

# Mock Database for Garments
GARMENTS = [
    {"id": "1", "name": "Traditional Kasavu Saree", "category": "saree", "price": 4500, "description": "Authentic Kerala Kasavu handloom cotton saree with golden zari border.", "image": "https://images.unsplash.com/photo-1610116306796-6fea9f4fae38?auto=format&fit=crop&w=500&q=80"},
    {"id": "2", "name": "Festive Silk Saree", "category": "saree", "price": 8900, "description": "Elegant silk saree with deep green and gold tones, perfect for festive occasions.", "image": "https://images.unsplash.com/photo-1583391733958-65021f1400d4?auto=format&fit=crop&w=500&q=80"},
    {"id": "3", "name": "Embroidered Cotton Churidhar", "category": "churidhar", "price": 2500, "description": "Comfortable pure cotton churidhar set with intricate threadwork.", "image": "https://images.unsplash.com/photo-1620016008685-a7db2bbf70ab?auto=format&fit=crop&w=500&q=80"},
    {"id": "4", "name": "Designer Anarkali Kurta", "category": "churidhar", "price": 3800, "description": "Beautiful flared anarkali suit for wedding functions.", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=500&q=80"},
    {"id": "5", "name": "Classic Blue Denim Jeans", "category": "jeans", "price": 2200, "description": "Premium stretchable classic blue denim for everyday wear.", "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=500&q=80"},
    {"id": "6", "name": "Slim Fit Black Jeans", "category": "jeans", "price": 2500, "description": "Stylish slim-fit black jeans for modern casual looks.", "image": "https://images.unsplash.com/photo-1596781741443-42bfbaef2f05?auto=format&fit=crop&w=500&q=80"},
    {"id": "7", "name": "Block Print Cotton Top", "category": "top", "price": 1200, "description": "Beautiful ethnic block print cotton top.", "image": "https://images.unsplash.com/photo-1529339396328-98e91d575797?auto=format&fit=crop&w=500&q=80"},
    {"id": "8", "name": "Trendy Georgette Kurti", "category": "top", "price": 1500, "description": "Lightweight georgette kurti in pastel shades.", "image": "https://images.unsplash.com/photo-1503341455253-b2e723bb3db8?auto=format&fit=crop&w=500&q=80"},
]

@app.get("/cakes")
def get_cakes():
    return GARMENTS

@app.get("/cakes/{item_id}")
def get_cake(item_id: str):
    for item in GARMENTS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

class Order(BaseModel):
    item: str
    quantity: int

@app.post("/order")
def create_order(order: Order):
    return {
        "message": "Order placed successfully!!",
        "order": order.dict(),
    }
