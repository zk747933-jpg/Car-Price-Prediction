import streamlit as st
import pandas as pd
import pickle
import os

# Page Config
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# -------- Load Files --------
MODEL_FILE = "model.pkl"
DATA_FILE = "cars.csv"

# Check files exist
if not os.path.exists(MODEL_FILE):
    st.error(f"❌ Missing file: {MODEL_FILE}")
    st.stop()

if not os.path.exists(DATA_FILE):
    st.error(f"❌ Missing file: {DATA_FILE}")
    st.stop()

# Load model and data
try:
    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)

    car = pd.read_csv(DATA_FILE)

except Exception as e:
    st.error(f"❌ Error loading files:\n{e}")
    st.stop()


# -------- Title --------
st.title("🚗 Car Price Predictor")
st.write("Enter car details below to predict price")


# Clean dropdown values
companies = sorted(car['company'].dropna().unique())
car_models = sorted(car['name'].dropna().unique())
years = sorted(car['year'].dropna().unique(), reverse=True)
fuel_types = sorted(car['fuel'].dropna().unique())


# -------- Inputs --------
company = st.selectbox(
    "Select Company",
    ["Select"] + list(companies)
)

car_model = st.selectbox(
    "Select Model",
    ["Select"] + list(car_models)
)

year = st.selectbox(
    "Select Year",
    ["Select"] + list(years)
)

fuel_type = st.selectbox(
    "Select Fuel Type",
    ["Select"] + list(fuel_types)
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=0,
    step=1000
)


# -------- Prediction --------
if st.button("Predict Price"):

    if (
        company == "Select"
        or car_model == "Select"
        or year == "Select"
        or fuel_type == "Select"
    ):

        st.warning("⚠ Please fill all fields")

    else:

        input_df = pd.DataFrame(
            [[
                car_model,
                company,
                int(year),
                km_driven,
                fuel_type
            ]],
            columns=[
                'name',
                'company',
                'year',
                'km_driven',
                'fuel'
            ]
        )

        try:
            prediction = model.predict(input_df)

            price = round(float(prediction[0]), 2)

            if price >= 10000000:
                display = f"{price/10000000:.2f} Crore"

            elif price >= 100000:
                display = f"{price/100000:.2f} Lakh"

            else:
                display = f"{price:,.2f}"

            st.success(f"💰 Predicted Price: ₹ {display}")

        except Exception as e:
            st.error(f"Prediction Error: {e}")
