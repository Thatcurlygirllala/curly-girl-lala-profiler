import os
import streamlit as st
import openai
from fpdf import FPDF

# -- Configuration --
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

OPENAI_MODEL = "gpt-4-turbo"
MAX_TOKENS = 200
TEMPERATURE = 0.7
import pathlib  
LOGO_PATH = str(pathlib.Path(__file__).parent / "cgl_logo.png")
APP_TITLE = "BrandVision Profiler by CGL"

st.set_page_config(page_title=APP_TITLE, layout="wide")

def display_logo():
    try:
        st.image(LOGO_PATH, use_container_width=True)  # Fixed deprecated warning
    except Exception:
        st.write("![CGL Logo](https://via.placeholder.com/150?text=CGL+Logo)")

@st.cache_data(show_spinner=False)
def get_pain_points(industry):
    prompt = f"Identify five key customer pain points in the {industry} industry or niche."
    try:
        response = openai.chat.completions.create(  # Updated OpenAI API format
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating pain points: {e}"

@st.cache_data(show_spinner=False)
def get_market_trends(industry):
    prompt = f"List five current market trends in the {industry} industry."
    try:
        response = openai.chat.completions.create(  # Updated OpenAI API format
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating market trends: {e}"

@st.cache_data(show_spinner=False)
def get_trending_topics(industry):
    prompt = f"In the {industry} industry, what are some emerging or trending topics currently generating buzz?"
    try:
        response = openai.chat.completions.create(  # Updated OpenAI API format
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating trending topics: {e}"

@st.cache_data(show_spinner=False)
def get_content_ideas(industry):
    prompt = f"Suggest three creative social media post ideas for a company in the {industry} niche."
    try:
        response = openai.chat.completions.create(  # Updated OpenAI API format
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS * 2,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating content ideas: {e}"

display_logo()
st.title("🚀 BrandVision Profiler by CGL")
st.markdown("""
### **Welcome to BrandVision Profiler by CGL!**
👋 Unlock powerful audience insights and content strategies in seconds!  
This AI-powered tool helps **entrepreneurs, consultants, and brand managers** discover:  
✅ **Key customer pain points** in your industry  
✅ **Emerging market trends** to stay ahead of competitors  
✅ **Trending topics** that drive engagement  
✅ **AI-generated social media content ideas** to boost visibility  

---
### **💰 Pricing Plans**
🔹 **Basic (Pay-Per-Search) – $5 per report**  
   - 1 competitor, 1 trending topic, basic insights  

🔹 **Pro Monthly Subscription – $15/month**  
   - Limited searches & features  

🔹 **Premium Monthly Subscription – $39/month**  
   - Unlimited searches & full AI-powered reports  

🔹 **Annual Premium – $390/year** (2 months free!)  
   - Full access at a discounted rate  

---
**📢 Start by entering your industry below & click "Generate Insights!"**
"")st.markdown("## Unlock AI-Powered Brand Insights")

industry = st.text_input("Enter an industry or niche:", placeholder="e.g. Coffee Shops, Sustainable Fashion")

results_container = st.container()

if st.button("Generate Insights") and industry.strip():
    with st.spinner("Generating insights..."):
        pain_points = get_pain_points(industry)
        trends = get_market_trends(industry)
        topics = get_trending_topics(industry)
        content_ideas = get_content_ideas(industry)
        st.session_state['pain_points'] = pain_points
        st.session_state['trends'] = trends
        st.session_state['topics'] = topics
        st.session_state['content_ideas'] = content_ideas

    with results_container:
        st.success(f"**Insights generated for:** {industry}")
        with st.expander("Customer Pain Points", expanded=True):
            st.write(st.session_state.get('pain_points', "No data available."))
        with st.expander("Market Trends", expanded=True):
            st.write(st.session_state.get('trends', "No data available."))
        with st.expander("Emerging Topics", expanded=True):
            st.write(st.session_state.get('topics', "No data available."))
        with st.expander("Social Media Content Ideas", expanded=True):
            st.write(st.session_state.get('content_ideas', "No data available."))

    st.markdown("----")
    st.subheader("Export Your Branded Report")
    if 'pain_points' in st.session_state:
        if st.button("Export Report"):
            pdf = FPDF()
            pdf.add_page()
            try:
                pdf.image(LOGO_PATH, x=10, y=8, w=30)
            except Exception:
                pass
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, APP_TITLE, ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Industry/Niche: {industry}", ln=True)
            pdf.ln(5)
            sections = ["Customer Pain Points", "Market Trends", "Emerging Topics", "Social Media Content Ideas"]
            for sec in sections:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, sec, ln=True)
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, str(st.session_state.get(sec.lower().replace(' ', '_'), "No data available.")))
                pdf.ln(5)
            pdf_data = pdf.output(dest='S').encode('latin1')
            st.download_button(label="📥 Download Report PDF", data=pdf_data, file_name=f"BrandVision_{industry}_Report.pdf", mime="application/pdf")
            st.success("Your BrandVision report is ready for download!")
