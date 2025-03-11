import sendgrid
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "your-sendgrid-key"

def send_branding_report(user_email, report_content):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    email = Mail(
        from_email="support@brandvisionprofiler.com",
        to_emails=user_email,
        subject="Your AI Branding Report is Ready!",
        html_content=f"<p>Here's your AI-powered branding report:</p><pre>{report_content}</pre>"
    )
    response = sg.send(email)
    return response.status_code
