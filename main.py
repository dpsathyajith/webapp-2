from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as google_firestore

# --- Firebase Setup ---
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Firebase on startup so the port binds before any SDK errors."""
    global db
    if os.path.exists("firebase-key.json"):
        # Initialize Firebase Admin (for other services if needed)
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
        # Initialize Firestore Client with named database
        db = google_firestore.Client.from_service_account_json("firebase-key.json", database="clothiqdb")
    else:
        # Initialize Firebase Admin (uses default credentials)
        firebase_admin.initialize_app()
        # Initialize Firestore Client with named database (uses environmental credentials)
        db = google_firestore.Client(database="clothiqdb")
    yield

# --- FastAPI Setup ---
app = FastAPI(lifespan=lifespan)

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
