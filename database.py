
reports = {}
earnings = {}

def store_report(user_id, report_content):
    reports[user_id] = report_content

def get_report(user_id):
    return reports.get(user_id, "No report found.")

def store_affiliate_referral(user_id, amount):
    earnings[user_id] = earnings.get(user_id, 0) + amount
