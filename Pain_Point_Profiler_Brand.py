

import streamlit as st
import openai
import stripe

# --- CONFIGURATION ---
OPENAI_API_KEY = "your_openai_api_key_here"  # Replace with your actual OpenAI API key
STRIPE_SECRET_KEY = "your_stripe_secret_key_here"  # Replace with your actual Stripe Secret Key
SUBSCRIPTION_PLANS = {
    "Basic": 3.99,
    "Pro": 12.00,
    "Premium": 29.00,
    "Annual": 290.00
}

stripe.api_key = STRIPE_SECRET_KEY

# Inject custom CSS for branding
st.markdown(
    """
    <style>
    .main { 
        background-color: #F8F5F6; 
        padding: 20px; 
    }
    h1, h2, h3 {
        color: #B58B95;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
    }
    p {
        font-size: 16px;
        line-height: 1.6;
        color: #2F2E2E;
    }
    .stButton>button {
        background-color: #B58B95;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>input {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to process one-time payment using Stripe Checkout
def process_payment():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Pain Point Profiler Search"},
                "unit_amount": int(5.00 * 100)
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel",
    )
    return session.url

# Function to process subscription payment using Stripe Checkout
def process_subscription(plan_name, price):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"Pain Point Profiler - {plan_name} Plan"},
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

# Dummy function for AI insights (replace with actual API call if desired)
def get_ai_insights(niche, question, content_format):
    if OPENAI_API_KEY == "your_openai_api_key_here":
        return "Sample AI-generated insights (OpenAI API call required)."
    else:
        # Implement your actual OpenAI API call here if needed
        return "Real AI-generated insights based on your input."

# Streamlit app layout
def app():
    st.image("logo.PNG", width=200)  # Replace with your logo path if available
    st.title("Pain Point Profiler - Advanced")
    st.header("Discover Your Audience's True Challenges")
    st.write(
        "Our AI-powered tool uncovers real audience pain points and delivers tailored content ideas "
        "to elevate your brand. Whether you're in coaching, digital marketing, or any niche, get actionable insights now."
    )
    
    st.subheader("Pricing Options")
    st.markdown("""
    **Pay Per Search:** $5 per search  
    **Subscription Plans:**  
    - Basic: $3.99/month  
    - Pro: $12/month  
    - Premium: $29/month  
    - Annual: $290/year  
    """)
    
    st.write("---")
    
    # Email capture for lead generation
    email = st.text_input("Enter your email to get a free preview:")
    if email:
        niche = st.text_input("Enter a niche (e.g., women in leadership, fitness coaches, tech startups):")
        question = st.text_input("Enter a specific question (optional):")
        brand_name = st.text_input("Enter your brand name (Optional for customized insights):")
        competitor_name = st.text_input("Enter a competitor's name (Optional for competitor analysis):")
        content_format = st.selectbox("Select content format:", 
                                      ["Social Media Post", "Blog Topic", "Video Idea", "Email Marketing Idea", "Podcast Episode"])
    
        if st.button("Get Free Preview"):
            if not niche:
                st.warning("Please enter a niche.")
            else:
                preview_result = get_ai_insights(niche, question, content_format)
                st.markdown("**Pain Point Insights:**\n" + preview_result.replace("-", "🔹"), unsafe_allow_html=True)
    
        st.write("---")
    
        # Payment options
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
    
if __name__ == "__main__":
    app()