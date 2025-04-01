import streamlit as st
import json
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1rVeFabNieHsKQS7zLZgpwisdiAUaOZX4uQ7BsuTKTHY")
worksheet = sheet.sheet1

# Productopties (inclusief groepoptie Citrus)
product_opties = [
    "Mangoes", "Avocados", "Oranges", "Lemons", "Limes",
    "Grapes", "Grapefruits", "Mandarins", "Pomelos",
    "Butternuts", "Ginger", "Citrus"
]

st.title("Subscribe to Market Reports")
st.write("Please fill in the form below to receive our weekly market updates.")

# Formulier
with st.form("subscribe_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company Name")

    st.markdown("### Address Information")
    col1, col2 = st.columns([3, 1])
    with col1:
        street = st.text_input("Street")
    with col2:
        street_nr = st.text_input("Number")

    col3, col4 = st.columns([2, 2])
    with col3:
        zip_code = st.text_input("Postal Code")
    with col4:
        city = st.text_input("City")

    address = f"{street} {street_nr}, {zip_code} {city}".strip(', ').strip()

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

            # Opslaan naar CSV
            try:
                df = pd.read_csv("subscribers.csv")
            except FileNotFoundError:
                df = pd.DataFrame()

            df = pd.concat([df, pd.DataFrame([subscriber])], ignore_index=True)
            df.to_csv("subscribers.csv", index=False)

            # Toevoegen aan Google Sheet
            worksheet.append_row([
                subscriber["timestamp"],
                subscriber["name"],
                subscriber["email"],
                subscriber["company"],
                subscriber["address"],
                ", ".join(subscriber["products"])
            ])

            st.success("You have been subscribed successfully!")
            st.balloons()

st.markdown("---")
st.write("Want to unsubscribe? [Click here](https://yourapp.streamlit.app/unsubscribe)")
