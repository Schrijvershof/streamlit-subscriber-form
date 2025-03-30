import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Laad productopties (inclusief "Citrus")
product_opties = [
    "Mangoes",
    "Avocados",
    "Oranges",
    "Lemons",
    "Limes",
    "Grapes",
    "Grapefruits",
    "Mandarins",
    "Pomelos",
    "Butternuts",
    "Ginger",
    "Citrus"  # Groepoptie
]

st.title("Subscribe to Market Reports")
st.write("Please fill in the form below to receive our weekly market updates.")

# Formulier
with st.form("subscribe_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company Name")
    address = st.text_area("Address")
    product_interest = st.multiselect("Product(s) of Interest", product_opties)

    submit = st.form_submit_button("Subscribe")

    if submit:
        if not name or not email or not product_interest:
            st.warning("Please fill in all required fields (Name, Email, Product).")
        else:
            subscriber = {
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "email": email,
                "company": company,
                "address": address,
                "products": product_interest
            }

            try:
                df = pd.read_csv("subscribers.csv")
            except FileNotFoundError:
                df = pd.DataFrame()

            df = pd.concat([df, pd.DataFrame([subscriber])], ignore_index=True)
            df.to_csv("subscribers.csv", index=False)

            st.success("You have been subscribed successfully!")
            st.balloons()

st.markdown("---")
st.write("Want to unsubscribe? [Click here](https://yourapp.streamlit.app/unsubscribe)")
