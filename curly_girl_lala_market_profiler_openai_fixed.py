

import streamlit as st
import openai
import stripe
import pyperclip

# --- CONFIGURATION ---
OPENAI_API_KEY = "import os OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET_KEY = "your_stripe_secret_key_here"  # Replace with your Stripe Secret Key
PRODUCT_PRICE = 5.00  # Pay-per-search price
PRO_PRICE = 15.00  # Pro Monthly Subscription price
PREMIUM_PRICE = 39.00  # Premium Monthly Subscription price
ANNUAL_PRICE = 390.00  # Annual Subscription price

stripe.api_key = STRIPE_SECRET_KEY

# Custom Streamlit Theme with a Vibrant and Engaging Look
st.set_page_config(page_title="Curly Girl LaLa’s Market Profiler", page_icon="🚀", layout="wide")

# Custom CSS Styling for Vibrant UI, Circular Profile Image, and Background Color
st.markdown(
    '''
    <style>
        body {
            background-color: #FFF5E1;
        }
        .profile-pic {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 130px;
            height: 130px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #FF5733;
        }
        .main-title {
            text-align: center;
            color: #FF5733;
            font-size: 42px;
            font-weight: bold;
            margin-top: 10px;
        }
        .sub-title {
            text-align: center;
            color: #FFC300;
            font-size: 24px;
        }
        .stButton>button {
            background-color: #FF5733 !important;
            color: white !important;
            border-radius: 10px;
            font-size: 18px;
            padding: 12px 24px;
            margin-top: 10px;
        }
        .stTextInput>div>div>input {
            border: 2px solid #FF5733;
            border-radius: 8px;
        }
        .block-container {
            padding: 30px;
        }
    </style>
    ''',
    unsafe_allow_html=True,
)

# Display centered, circular profile picture
st.markdown(
    f'<img src="https://i.imgur.com/0K2vyGo.jpg" class="profile-pic">',
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>Curly Girl LaLa’s Market Profiler</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-title'>🔥 Discover Your Market's Pain Points & Growth Strategies! 🔥</h2>", unsafe_allow_html=True)
st.write("🚀 Gain deep insights into your niche, find trending topics, and create high-converting content!")

# Section 1: Market Insights
st.markdown(
    "<div style='background-color:#FFE4B5; padding: 20px; border-radius: 10px;'>"
    "<h2 style='color:#D35400;'>📊 Identify Your Market’s Biggest Pain Points</h2>"
    "<p>Auto-generate common challenges faced by your target audience.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# Niche Input
niche = st.text_input("🎯 Enter a niche (e.g., Leadership, Fitness Coaches, Startups, Real Estate):")

# Function to get AI-powered insights
def get_ai_insights(niche, pain_point, content_format, analysis_type):
    openai.api_key = OPENAI_API_KEY

    prompt = f"""Generate insights for the niche '{niche}' based on '{analysis_type}'. 
    Focus on the pain point: '{pain_point}'. Include:
    - A key question the audience might ask.
    - A {content_format} idea to address that pain point.
    - Competitor analysis insights.
    - Audience & buyer persona details.
    - Market positioning & unique selling proposition recommendations.
    - Email & funnel strategy suggestions.
    - Trending content ideas & best-performing formats.

    Format:
    1. {analysis_type}: [Generated Insights]
    """

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in business market research."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content

# Function to auto-suggest pain points for a given niche
def suggest_pain_points(niche):
    openai.api_key = OPENAI_API_KEY

    prompt = f"List the top 5 common pain points for the niche: '{niche}'."

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in audience research."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.split("\n")

# Generate Pain Points Section
suggested_pain_points = []
if st.button("🚀 Generate Pain Points"):
    if not niche:
        st.warning("⚠️ Please enter a niche.")
    else:
        suggested_pain_points = suggest_pain_points(niche)
        st.write("### 🎯 Suggested Pain Points:")
        for point in suggested_pain_points:
            st.write(f"- {point}")

pain_point = st.selectbox("🔍 Select a pain point:", suggested_pain_points if suggested_pain_points else ["Enter manually"])
if pain_point == "Enter manually":
    pain_point = st.text_input("💡 Or enter a custom pain point:")

content_format = st.selectbox("🎨 Select content format:", ["Social Media Post", "Blog Topic", "Video Idea", "Email Marketing Idea", "Podcast Episode"])
analysis_type = st.selectbox("📊 Select Analysis Type:", ["Audience & Buyer Persona", "Trending Topics", "Competitive Analysis", "Market Positioning", "AI-Powered Social Media & Ad Copy", "Email & Funnel Strategy"])

if st.button("🔥 Get Free Preview"):
    if not niche or not pain_point:
        st.warning("⚠️ Please enter a niche and select a pain point.")
    else:
        st.write(f"### 🔥 Free Preview for '{niche}' - Pain Point: {pain_point}")
        preview_result = get_ai_insights(niche, pain_point, content_format, analysis_type)
        st.text_area("🎯 Sample Result", preview_result, height=200)

        # Add "Copy to Clipboard" button
        if st.button("📋 Copy to Clipboard"):
            pyperclip.copy(preview_result)
            st.success("✅ Copied to clipboard!")

st.write("---")

# Define the app function to avoid errors
def app():
    pass

if __name__ == "__main__":
    app()

