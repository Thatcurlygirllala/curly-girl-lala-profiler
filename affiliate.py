import stripe

stripe.api_key = "your-stripe-secret-key"

def create_affiliate_link(user_id):
    return f"https://brandvisionprofiler.com/register?ref={user_id}"

def track_affiliate_purchase(referrer_id, commission=10):
    return f"Commission of ${commission} added to {referrer_id}."
