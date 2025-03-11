import openai

ai_role = """
You are an AI-powered Branding & Social Media Marketing expert. Your expertise includes:
- Brand positioning & audience engagement.
- Competitor analysis & differentiation strategies.
- Viral social media content creation.
- AI-powered paid ads for Instagram, Facebook, and LinkedIn.
"""

def generate_branding_strategy(user_input):
    prompt = f"""
    Branding Request: {user_input}
    - Unique brand positioning strategy
    - Top 3 audience pain points
    - Competitor weaknesses & how to differentiate
    - Viral content strategy for LinkedIn & Instagram
    - CTA-driven messaging approach
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": ai_role}, {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
