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
    {"id": "1", "name": "Kanchipuram Silk Saree", "category": "saree", "price": 12500, "description": "Authentic handwoven Kanchipuram silk saree with pure zari border.", "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=500&q=80"},
    {"id": "2", "name": "Banarasi Georgette Saree", "category": "saree", "price": 8900, "description": "Elegant Banarasi georgette saree, perfect for festive occasions.", "image": "https://images.unsplash.com/photo-1583391733958-65021f1400d4?auto=format&fit=crop&w=500&q=80"},
    {"id": "3", "name": "Embroidered Anarkali Churidhar", "category": "churidhar", "price": 4500, "description": "Beautiful flared anarkali suit with heavy embroidery.", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=500&q=80"},
    {"id": "4", "name": "Cotton Printed Churidhar", "category": "churidhar", "price": 1800, "description": "Comfortable daily-wear pure cotton printed churidhar set.", "image": "https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=500&q=80"},
    {"id": "5", "name": "Classic Blue Denim Jeans", "category": "jeans", "price": 2200, "description": "Premium stretchable classic blue denim for everyday wear.", "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=500&q=80"},
    {"id": "6", "name": "High-Waist Black Jeans", "category": "jeans", "price": 2500, "description": "Stylish high-waist black skinny jeans.", "image": "https://images.unsplash.com/photo-1596781741443-42bfbaef2f05?auto=format&fit=crop&w=500&q=80"},
    {"id": "7", "name": "Floral Chiffon Top", "category": "top", "price": 1200, "description": "Lightweight breathable floral chiffon top.", "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=500&q=80"},
    {"id": "8", "name": "Ribbed Crop Top", "category": "top", "price": 800, "description": "Trendy ribbed crop top in earthy tones.", "image": "https://images.unsplash.com/photo-1503341455253-b2e723bb3db8?auto=format&fit=crop&w=500&q=80"},
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
