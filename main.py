from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase Setup ---
# Use service account key file if it exists (local dev)
# On Cloud Run, use default credentials
if os.path.exists("firebase-key.json"):
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()  # Uses Cloud Run's built-in credentials

db = firestore.client(database="clothiqdb")

# --- FastAPI Setup ---
app = FastAPI()

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/cakes")
def get_all_garments():
    """Fetch ALL products from Firestore."""
    docs = db.collection("garments").stream()
    garments = []
    for doc in docs:
        garment = doc.to_dict()
        garment["id"] = doc.id       # Add the document ID
        garments.append(garment)
    return garments

@app.get("/cakes/{item_id}")
def get_one_garment(item_id: str):
    """Fetch ONE product from Firestore by ID."""
    doc = db.collection("garments").document(item_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")
    garment = doc.to_dict()
    garment["id"] = doc.id
    return garment

class Order(BaseModel):
    item: str
    quantity: int

@app.post("/order")
def create_order(order: Order):
    return {
        "message": "Order placed successfully!!",
        "order": order.dict(),
    }
