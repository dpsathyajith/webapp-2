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
# Images are served from the Next.js frontend /public folder
FRONTEND_BASE = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

GARMENTS = [
    {"id": "1", "name": "Traditional Kasavu Saree", "category": "saree", "price": 1100, "description": "Authentic Kerala Kasavu handloom cotton saree with golden zari border.", "image": f"{FRONTEND_BASE}/kasavu-saree.png"},
    {"id": "2", "name": "Festive Silk Saree", "category": "saree", "price": 1200, "description": "Elegant silk saree with deep green and gold tones, perfect for festive occasions.", "image": f"{FRONTEND_BASE}/festive-silk-saree.png"},
    {"id": "3", "name": "Embroidered Cotton Churidhar", "category": "churidhar", "price": 750, "description": "Comfortable pure cotton churidhar set with intricate threadwork.", "image": f"{FRONTEND_BASE}/churidhar-cotton.png"},
    {"id": "4", "name": "Designer Anarkali Kurta", "category": "churidhar", "price": 950, "description": "Beautiful flared anarkali suit for wedding functions.", "image": f"{FRONTEND_BASE}/anarkali-kurta.png"},
    {"id": "5", "name": "Classic Blue Denim Jeans", "category": "jeans", "price": 800, "description": "Premium stretchable classic blue denim for everyday wear.", "image": "https://images.pexels.com/photos/1082529/pexels-photo-1082529.jpeg?auto=compress&cs=tinysrgb&w=500"},
    {"id": "6", "name": "Slim Fit Black Jeans", "category": "jeans", "price": 900, "description": "Stylish slim-fit black jeans for modern casual looks.", "image": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=500"},
    {"id": "7", "name": "Block Print Cotton Top", "category": "top", "price": 500, "description": "Beautiful ethnic block print cotton top.", "image": "https://images.pexels.com/photos/6311392/pexels-photo-6311392.jpeg?auto=compress&cs=tinysrgb&w=500"},
    {"id": "8", "name": "Trendy Georgette Kurti", "category": "top", "price": 650, "description": "Lightweight georgette kurti in pastel shades.", "image": "https://images.pexels.com/photos/7679863/pexels-photo-7679863.jpeg?auto=compress&cs=tinysrgb&w=500"},
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
