

import streamlit as st
import openai
import stripe
import pdfkit

# --- CONFIGURATION ---
OPENAI_API_KEY = "your_openai_api_key_here"  # Replace with your OpenAI API key
STRIPE_SECRET_KEY = "your_stripe_secret_key_here"  # Replace with your Stripe Secret Key
SUBSCRIPTION_PLANS = {
    "Basic": 3.99,
    "Pro": 12.00,
    "Premium": 29.00,
    "Annual": 290.00
}

stripe.api_key = STRIPE_SECRET_KEY

# Function to process one-time payment
def process_payment():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "usd", "product_data": {"name": "Pain Point Profiler Search"},
                                    "unit_amount": int(5.00 * 100)},
                     "quantity": 1}],
        mode="payment",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel",
    )
    return session.url

# Function to process subscription payment
def process_subscription(plan_name, price):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "usd", "product_data": {"name": f"Pain Point Profiler - {plan_name} Plan"},
                                    "unit_amount": int(price * 100), "recurring": {"interval": "month"}}],
        mode="subscription",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel",
    )
    return session.url

# Function to generate insights using OpenAI API
def get_ai_insights(niche, question, content_format, brand_name, competitor_name):
    openai.api_key = OPENAI_API_KEY

    prompt = f"Generate a list of pain points for the niche: {niche}."
    
    if brand_name:
        prompt += f" Customize these insights specifically for the brand '{brand_name}'."

    if competitor_name:
        prompt += f" Also, analyze the weaknesses of '{competitor_name}' and provide strategies for gaining a competitive advantage."

    prompt += f"
For each pain point, generate:
- A key audience question.
- A {content_format} idea.
"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in audience research."},
                  {"role": "user", "content": prompt}],
        max_tokens=600
    )

    return response["choices"][0]["message"]["content"]

# Streamlit app layout
def app():
    st.title("Pain Point Profiler - Advanced")
    st.write("Enter a niche or specific question to discover pain points, key questions, and content ideas!")

    # Email Capture Before Free Preview
    email = st.text_input("Enter your email to get a free preview:")

    if email:
        niche = st.text_input("Enter a niche (e.g., women in leadership, fitness coaches, tech startups):")
        question = st.text_input("Enter a specific question (optional):")
        brand_name = st.text_input("Enter your brand name (Optional for customized insights):")
        competitor_name = st.text_input("Enter a competitor's name (Optional for competitor analysis):")
        content_format = st.selectbox("Select content format:", ["Social Media Post", "Blog Topic", "Video Idea", "Email Marketing Idea", "Podcast Episode"])

        if st.button("Get Free Preview"):
            if not niche:
                st.warning("Please enter a niche.")
            else:
                st.write(f"### Free Preview for '{niche}'")
                preview_result = get_ai_insights(niche, question, content_format, brand_name, competitor_name)
                st.markdown(f"**Pain Point Insights:**

{preview_result.replace('-', '🔹')}", unsafe_allow_html=True)

        st.write("---")

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

        # Download as PDF Button
        if st.button("Download Insights as PDF"):
            pdf_filename = f"{niche.replace(' ', '_')}_Insights.pdf"
            pdf_content = f"Pain Point Profiler Insights for {niche}

{preview_result}"
            with open(pdf_filename, "w") as pdf_file:
                pdf_file.write(pdf_content)
            st.success(f"Download your insights here: [**{pdf_filename}**]")

        # Done-for-You Content Upgrade
        st.write("### 🚀 Upgrade: Get AI-Written Content!")
        st.write("Want full content posts instead of just ideas? Upgrade to **Done-for-You AI Content** where AI generates full posts for you!")
        if st.button("Upgrade to Done-for-You AI Content ($19 per post)"):
            st.markdown("[Click here to purchase](#)", unsafe_allow_html=True)

        # VIP Coaching Hub
        st.write("### 🔥 VIP Coaching Hub (Exclusive Access)")
        st.write("Join our **Premium Membership** for **weekly content trends & AI-powered insights**.")
        if st.button("Join VIP Coaching Hub ($99/month)"):
            st.markdown("[Click here to subscribe](#)", unsafe_allow_html=True)

        # FAQ Section
        st.write("---")
        st.write("### ❓ Frequently Asked Questions")
        st.write("**How does the Pain Point Profiler work?**
"
                 "Simply enter a niche or question, and AI will generate pain points, audience questions, and content ideas for you.")
        st.write("**What happens after I pay?**
"
                 "You'll instantly receive full AI-generated insights tailored to your audience.")
        st.write("**Can I cancel my subscription?**
"
                 "Yes! You can cancel anytime from your account settings.")
        st.write("**Is my payment secure?**
"
                 "Absolutely! We use **Stripe** for secure payments and never store your financial details.")

if __name__ == "__main__":
    app()

