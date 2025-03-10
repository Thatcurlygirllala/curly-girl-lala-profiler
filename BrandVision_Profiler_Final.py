
# BrandVision Profiler - AI-Powered Audience Research & Content Generator
# Fully Integrated with Airtable, Stripe Payments, AI Features, and Admin Back Office

import os
import streamlit as st
import requests
import openai
import stripe
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- API KEYS & CONFIGURATION ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "Client Management"
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY
openai.api_key = OPENAI_API_KEY

# --- ACCESS CODES & FREE TRIAL SETTINGS ---
ACCESS_CODES = {
    "TEST100": {"days": 7, "level": "Full", "extendable": True},
    "VIPACCESS": {"days": 3, "level": "Pro", "extendable": False}
}

# --- FUNCTION: CHECK OR ADD USER TO AIRTABLE ---
def check_or_add_airtable_access(email, access_code=None):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}

    today = datetime.now().strftime("%Y-%m-%d")

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json().get("records", [])
        for record in records:
            fields = record.get("fields", {})
            if fields.get("Email") == email:
                expiration_date = fields.get("Expiration Date", today)
                usage_count = fields.get("Usage Count", 0)
                access_level = fields.get("Access Level", "None")

                if fields.get("Access Status") == "Active":
                    if datetime.strptime(expiration_date, "%Y-%m-%d") >= datetime.now():
                        if access_level == "Full" and fields.get("Extendable") and usage_count >= 3:
                            new_expiration = (datetime.strptime(expiration_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
                            update_data = {"records": [{"id": record["id"], "fields": {"Expiration Date": new_expiration}}]}
                            update_response = requests.patch(url, headers=headers, json=update_data)
                            if update_response.status_code == 200:
                                return access_level, new_expiration, "Extended"
                        return access_level, expiration_date, "Active"
                    else:
                        return None, expiration_date, "Expired"

    if access_code in ACCESS_CODES:
        trial_days = ACCESS_CODES[access_code]["days"]
        access_level = ACCESS_CODES[access_code]["level"]
        extendable = ACCESS_CODES[access_code]["extendable"]
        expiration_date = (datetime.now() + timedelta(days=trial_days)).strftime("%Y-%m-%d")
    else:
        return None, None, "Invalid Code"

    data = {
        "records": [
            {
                "fields": {
                    "Email": email,
                    "Signup Date": today,
                    "Expiration Date": expiration_date,
                    "Access Level": access_level,
                    "Extendable": extendable,
                    "Access Status": "Active",
                    "Usage Count": 0
                }
            }
        ]
    }

    add_response = requests.post(url, headers=headers, json=data)
    if add_response.status_code == 200:
        return access_level, expiration_date, "New"
    else:
        return None, None, "Error"

# --- STREAMLIT UI ---
st.image("B.png", width=200, use_column_width="auto")
st.title("BrandVision Profiler")
st.header("Unlock the Secrets to What Your Audience Wants")

email = st.text_input("Enter your email for free access:")
access_code = st.text_input("Enter your access code (if provided):")

if email:
    access_level, expiration_date, status = check_or_add_airtable_access(email, access_code)

    if access_level:
        if status == "Extended":
            st.success(f"✅ Your trial has been extended! Your access expires on {expiration_date}.")
        else:
            st.success(f"✅ {access_level} access granted! Your trial expires on {expiration_date}.")

# --- ADMIN BACK OFFICE ---
st.sidebar.header("Admin Back Office")
admin_email = st.sidebar.text_input("curlygirllala@gmail.com:")

if admin_email == "curlygirllala@gmail.com":
    st.sidebar.success("✅ Admin Access Granted")

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users = response.json().get("records", [])
        st.sidebar.write(f"📌 **Total Users:** {len(users)}")

        for user in users:
            fields = user.get("fields", {})
            email = fields.get("Email", "N/A")
            access_level = fields.get("Access Level", "N/A")
            expiration_date = fields.get("Expiration Date", "N/A")
            status = fields.get("Access Status", "N/A")

            st.sidebar.write(f"📌 **{email}** | **{access_level}** | Exp: {expiration_date} | Status: {status}")
