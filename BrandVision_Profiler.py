

import streamlit as st
import openai
import stripe
import os

# --- CONFIGURATION ---
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely store API key in Render environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Securely store Stripe API key

SUBSCRIPTION_PLANS = {
    "Basic": 3.99,
    "Pro": 12.00,
    "Premium": 29.00,
    "Annual": 290.00
}

# --- CUSTOM CSS FOR BRANDING ---
st.markdown(
    """
    <style>
    .main { background-color: #F8F5F6; padding: 20px; }
    h1, h2, h3 { color: #B58B95; font-family: 'Helvetica', sans-serif; font-weight: bold; }
    p { font-size: 16px; line-height: 1.6; color: #2F2E2E; }
    .stButton>button { background-color: #B58B95; color: white; border-radius: 8px; padding: 10px 20px; font-size: 16px; }
    .stTextInput>div>input { border: 1px solid #ccc; border-radius: 4px; padding: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FUNCTION TO FETCH AI-POWERED PAIN POINTS ---
def get_ai_insights(business_type, question, content_format):
    """ Calls OpenAI API to generate pain points and content ideas. """
    
    prompt = f"Generate 3 audience pain points for {business_type}. Focus on market gaps, common frustrations, and business challenges. Format as bullet points."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert marketing strategist."},
                {"role": "user", "content": prompt}
            ]
        )
        insights = response["choices"][0]["message"]["content"]
        return insights
    except Exception as e:
        return f"Error fetching AI insights: {str(e)}"

# --- FUNCTION TO PROCESS PAYMENTS ---
def process_payment():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "BrandVision Profiler Search"},
                "unit_amount": int(5.00 * 100)
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel",
    )
    return session.url

def process_subscription(plan_name, price):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"BrandVision Profiler - {plan_name} Plan"},
                "unit_amount": int(price * 100),
                "recurring": {"interval": "month"}
            },
            "quantity": 1
        }],
        mode="subscription",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel",
    )
    return session.url

# --- STREAMLIT APP LAYOUT ---
st.image("logo.svg", width=200, use_column_width="auto")  # Update with your correct logo path
st.title("BrandVision Profiler")
st.header("Unlock the Secrets to What Your Audience Wants")

st.write(
    "Confused about what your audience truly needs? Stop guessing. Our AI-powered BrandVision Profiler scans "
    "market trends, customer frustrations, and competitor weaknesses to uncover profitable pain points. Get "
    "instant insights, tailored content ideas, and a clear strategy—so you can attract and convert the right clients effortlessly."
)

st.subheader("Instant Insights—No Payment Required")
st.write("Get a sneak peek into audience pain points before unlocking full insights.")

# --- FREE PREVIEW INPUT SECTION ---
email = st.text_input("Enter your email to get a free preview:")

if email:
    business_type = st.text_input("Enter your business type (e.g., coaching, marketing, e-commerce, real estate):")
    question = st.text_input("Enter a specific question (optional):")
    content_format = st.selectbox("Select content format:", 
                                  ["Social Media Post", "Blog Topic", "Video Idea", "Email Marketing Idea", "Podcast Episode"])

    if st.button("Get Free Preview"):
        if not business_type:
            st.warning("Please enter your business type.")
        else:
            preview_result = get_ai_insights(business_type, question, content_format)
            st.markdown("### Preview: First Pain Point Insight")
            st.write(preview_result.split("\n")[0])  # Shows only the first bullet point
            st.markdown("🔓 **Unlock full insights** with a search or subscription below!")

    st.write("---")

    # --- PAYMENT OPTIONS ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Pay Per Search ($5)"):
            payment_url = process_payment()
            st.markdown(f"[Click here to complete payment]({payment_url})", unsafe_allow_html=True)

    with col2:
        selected_plan = st.selectbox("Choose a Subscription Plan:", list(SUBSCRIPTION_PLANS.keys()))
        if st.button(f"Subscribe - {selected_plan} Plan"):
            subscription_url = process_subscription(selected_plan, SUBSCRIPTION_PLANS[selected_plan])
            st.markdown(f"[Click here to subscribe]({subscription_url})", unsafe_allow_html=True)

st.write("---")

st.subheader("Pricing Options")
st.markdown("""
**Pay Per Search:** $5 per search  
**Subscription Plans:**  
- Basic: $3.99/month  
- Pro: $12/month  
- Premium: $29/month  
- Annual: $290/year  
""")

if __name__ == "__main__":
    app()