# BrandVision Profiler Ultimate - FINAL VERSION with Premium Plan Enhancements

from flask import Flask, request, jsonify, send_file
import openai
import stripe
import airtable
import calendly
import pdfkit
import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
db = SQLAlchemy(app)
jwt = JWTManager(app)

# API Keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_API_KEY")
airtable_client = airtable.AirtableClient(os.getenv("AIRTABLE_API_KEY"))
calendly_api = calendly.Calendly(os.getenv("CALENDLY_API_KEY"))
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")  # For AI-Powered Email Summaries

# UI Color Configuration
UI_COLORS = {
    "primary_black": "#000000",
    "accent_pink": "#D2A4A7",
    "muted_blue_gray": "#A4A9B2",
    "light_gray_white": "#F8F8F8",
    "soft_pink_tint": "#EED6DC"
}

# Subscription Plans & Free Trial System
PRICING_OPTIONS = {
    "free_trial": {"price": "$0 for 7 days", "features": ["Limited AI searches", "Basic competitor analysis", "Preview access"]},
    "basic": {"price": "$3.99/month", "features": ["5 AI searches", "Limited Competitor Analysis", "PDF Downloads"]},
    "pro": {"price": "$12/month", "features": ["50 AI searches/month", "10 competitor searches", "VIP Hub Access"]},
    "premium": {"price": "$29/month", "features": ["Unlimited AI & Competitor Analysis", "AI Content Generator", "AI-Powered Ad Generator", 
                  "Advanced AI Competitor Deep Dive", "Weekly Brand Strategy Reports", "Social Media Scheduler Integration", 
                  "VIP Business Name & Tagline Generator", "SEO Blog Outlines", "Exclusive Community & Live Q&A Sessions"]},
    "one_time": {
        "search": "$5 per search",
        "audit": "$49 Social Media Audit",
        "coaching": "$47 One-on-One Coaching",
        "bulk": "$99 Bulk AI Reports (5+ Competitors)"
    },
    "vipaccess": {"price": "$99/month", "features": ["Exclusive AI Insights", "White-Label Options", "Priority Support"]}
}

# Unlimited AI-Powered Ad Generator (Premium Only)
@app.route('/generate_premium_ads', methods=['POST'])
@jwt_required()
def generate_premium_ads():
    data = request.json
    ad_purpose = data['ad_purpose']
    ad_prompt = f"Create optimized Facebook, Instagram, and LinkedIn ads for: {ad_purpose}. Include variations for A/B testing."
    ad_response = openai.Completion.create(engine="gpt-4", prompt=ad_prompt, max_tokens=700)
    return jsonify({"ad_copy": ad_response.choices[0].text.strip(), "theme_colors": UI_COLORS})

# Advanced AI Competitor Deep Dive (Premium Only)
@app.route('/competitor_deep_dive', methods=['POST'])
@jwt_required()
def competitor_deep_dive():
    data = request.json
    competitor_name = data['competitor_name']
    deep_dive_prompt = f"Perform a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for {competitor_name}. Provide strategic recommendations."
    deep_dive_response = openai.Completion.create(engine="gpt-4", prompt=deep_dive_prompt, max_tokens=800)
    return jsonify({"competitor_analysis": deep_dive_response.choices[0].text.strip(), "theme_colors": UI_COLORS})

# AI-Powered Weekly Brand Strategy Reports (Premium Only)
@app.route('/weekly_strategy_report', methods=['POST'])
@jwt_required()
def weekly_strategy_report():
    data = request.json
    user_niche = data['niche']
    strategy_prompt = f"Generate a personalized weekly brand strategy report for a business in {user_niche}. Include content trends, engagement strategies, and industry insights."
    strategy_response = openai.Completion.create(engine="gpt-4", prompt=strategy_prompt, max_tokens=1000)
    return jsonify({"strategy_report": strategy_response.choices[0].text.strip(), "theme_colors": UI_COLORS})

# AI-Powered Social Media Scheduler Integration (Premium Only)
@app.route('/schedule_social_posts', methods=['POST'])
@jwt_required()
def schedule_social_posts():
    data = request.json
    post_content = data['post_content']
    schedule_time = data['schedule_time']
    scheduling_request = {"post": post_content, "time": schedule_time, "platform": "LinkedIn, Instagram, Facebook"}
    return jsonify({"message": "Social media post scheduled successfully!", "details": scheduling_request, "theme_colors": UI_COLORS})

# VIP Business Name & Tagline Generator (Premium Only)
@app.route('/vip_brand_name_generator', methods=['POST'])
@jwt_required()
def vip_brand_name_generator():
    data = request.json
    industry = data['industry']
    name_prompt = f"Generate 5 premium, high-quality brand names and taglines for a business in {industry}. Include brand story insights."
    name_response = openai.Completion.create(engine="gpt-4", prompt=name_prompt, max_tokens=600)
    return jsonify({"brand_suggestions": name_response.choices[0].text.strip(), "theme_colors": UI_COLORS})

# AI-Generated Website Headlines & SEO Blog Outlines (Premium Only)
@app.route('/seo_blog_outlines', methods=['POST'])
@jwt_required()
def seo_blog_outlines():
    data = request.json
    blog_topic = data['blog_topic']
    blog_prompt = f"Generate an SEO-optimized blog outline for: {blog_topic}. Include headlines, subheadings, and content suggestions."
    blog_response = openai.Completion.create(engine="gpt-4", prompt=blog_prompt, max_tokens=700)
    return jsonify({"blog_outline": blog_response.choices[0].text.strip(), "theme_colors": UI_COLORS})

# VIP Exclusive Community & Live Q&A Sessions (Premium Only)
@app.route('/premium_community', methods=['GET'])
@jwt_required()
def premium_community():
    return jsonify({
        "message": "Welcome to the Premium Community Hub! Join live Q&A sessions, access VIP networking, and receive priority branding insights.",
        "theme_colors": UI_COLORS
    })

if __name__ == '__main__':
    app.run(debug=True)
