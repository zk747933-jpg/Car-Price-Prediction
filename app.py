import streamlit as st
import pandas as pd
import pickle

# Page settings
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# Load model
try:
    model = pickle.load(open('model.pkl', 'rb'))
    car = pd.read_csv('cars.csv')
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()


st.title("🚗 Car Price Predictor")
st.write("Enter car details to predict price")

# Dropdown values
companies = sorted(car['company'].unique())
car_models = sorted(car['name'].unique())
years = sorted(car['year'].unique(), reverse=True)
fuel_types = sorted(car['fuel'].unique())


# Inputs
company = st.selectbox(
    "Select Company",
    ["Select"] + companies
)

car_model = st.selectbox(
    "Select Model",
    ["Select"] + car_models
)

year = st.selectbox(
    "Select Year",
    ["Select"] + list(years)
)

fuel_type = st.selectbox(
    "Select Fuel Type",
    ["Select"] + fuel_types
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    step=1000
)


# Predict button
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
            [[car_model,
              company,
              int(year),
              km_driven,
              fuel_type]],
            columns=[
                'name',
                'company',
                'year',
                'km_driven',
                'fuel'
            ]
        )

        prediction = model.predict(input_df)
        price = round(prediction[0], 2)

        if price >= 10000000:
            formatted_price = f"{price/10000000:.2f} Crore"

        elif price >= 100000:
            formatted_price = f"{price/100000:.2f} Lakh"

        else:
            formatted_price = f"{price:,.2f}"

        st.success(
            f"💰 Predicted Price: ₹ {formatted_price}"
        )
