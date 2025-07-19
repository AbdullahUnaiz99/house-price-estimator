import streamlit as st
import requests as rs

# Backend URL (make sure your FastAPI server is running here)
BACKEND_URL = "http://127.0.0.1:8000"

# Center the title
st.markdown("""
    <h1 style='text-align: center;'>🏠 Bangalore House Price Estimator</h1>
""", unsafe_allow_html=True)


def load_locations():
    """
    Fetch list of locations from backend.
    """
    try:
        res = rs.get(f"{BACKEND_URL}/get_location_names")
        if res.status_code == 200:
            return res.json().get("locations", [])
        else:
            st.error(f"Failed to fetch locations: Status {res.status_code}")
    except Exception as e:
        st.error(f"Error contacting backend: {e}")
    return []

def main():
    
    # Load locations from backend
    locations = load_locations()
    if not locations:
        st.warning("Could not load locations. Is the backend running?")

    # User inputs
    total_sqft = st.number_input(
        "Total Square Feet", 
        min_value=300, max_value=30000, value=1000, step=10
    )

    bhk = st.selectbox(
        "Number of Bedrooms", 
        list(range(1, 17)), index=0  # default 1 BHK
    )

    bath = st.selectbox(
        "Number of Bathrooms", 
        list(range(1, 17)), index=0  # default 1 bathrooms
    )

    location = st.selectbox(
        "Location", 
        sorted(locations) if locations else ["Loading..."]
    )

    # Predict button
    if st.button("Get Estimate"):

        data = {
            "total_sqft": total_sqft,
            "location": location,
            "bhk": bhk,
            "bath": bath
        }
        try:
            res = rs.post(f"{BACKEND_URL}/predict_home_price", data=data)
            if res.status_code == 200:
                estimated_price = res.json().get("estimated_price")
                if estimated_price is not None:
                    st.success(f"💰 Estimated Price: ₹ {estimated_price} lakhs")
                else:
                    st.warning("Could not calculate price. Check your input.")
            else:
                st.error(f"Backend error: Status {res.status_code}")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")

if __name__ == "__main__":
    main()
