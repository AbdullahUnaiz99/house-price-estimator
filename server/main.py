# server/main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import util

app = FastAPI(
    title="🏠 House Price Prediction API",
    description="Predict house prices based on location, sqft, BHK, and bath.",
    version="1.0.0"
)

# Enable CORS (allow frontend like Streamlit to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to your domain if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_artifacts():
    util.load_saved_artifacts()

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running."}

@app.get("/get_location_names")
def get_location_names():
    locations = util.get_location_names()
    return {"locations": locations}

@app.post("/predict_home_price")
def predict_home_price(
    total_sqft: float = Form(...),
    location: str = Form(...),
    bhk: int = Form(...),
    bath: int = Form(...)
):
    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
    return {"estimated_price": estimated_price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
