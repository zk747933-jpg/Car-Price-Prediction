import streamlit as st
import pandas as pd
import pickle
import os

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# ---------------- FILE NAMES ----------------
MODEL_FILE = "model.pkl"
DATA_FILE = "cars.csv"

# ---------------- CHECK FILES ----------------
missing_files = []

if not os.path.exists(MODEL_FILE):
    missing_files.append(MODEL_FILE)

if not os.path.exists(DATA_FILE):
    missing_files.append(DATA_FILE)

if missing_files:
    st.error(f"Missing files: {', '.join(missing_files)}")
    st.stop()


# ---------------- LOAD MODEL + DATA ----------------
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    car = pd.read_csv(DATA_FILE)

except Exception as e:
    st.error(f"Error loading files:\n{e}")
    st.stop()


# ---------------- TITLE ----------------
st.title("🚗 Car Price Predictor")
st.markdown("Enter car details and predict estimated price")


# ---------------- CLEAN DATA ----------------
car = car.dropna()

companies = sorted(car["company"].unique())
models = sorted(car["name"].unique())
years = sorted(car["year"].unique(), reverse=True)
fuel_types = sorted(car["fuel"].unique())


# ---------------- INPUTS ----------------
company = st.selectbox(
    "Select Company",
    ["Select"] + list(companies)
)

model_name = st.selectbox(
    "Select Model",
    ["Select"] + list(models)
)

year = st.selectbox(
    "Select Year",
    ["Select"] + list(years)
)

fuel = st.selectbox(
    "Select Fuel Type",
    ["Select"] + list(fuel_types)
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=0,
    step=1000
)


# ---------------- PREDICTION ----------------
if st.button("Predict Price"):

    if (
        company == "Select"
        or model_name == "Select"
        or year == "Select"
        or fuel == "Select"
    ):

        st.warning("⚠ Please fill all fields")

    else:

        input_df = pd.DataFrame(
            [[
                model_name,
                company,
                int(year),
                km_driven,
                fuel
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

            price = float(prediction[0])

            if price < 0:
                price = abs(price)

            if price >= 10000000:
                display = f"{price/10000000:.2f} Crore"

            elif price >= 100000:
                display = f"{price/100000:.2f} Lakh"

            else:
                display = f"{price:,.2f}"

            st.success(
                f"💰 Estimated Price: ₹ {display}"
            )

        except Exception as e:
            st.error(f"Prediction Error: {e}")
