from flask import Flask, request, jsonify
from ai_engine import generate_branding_strategy
from email_service import send_branding_report
from database import store_report, get_report

app = Flask(__name__)

@app.route("/generate-branding-strategy", methods=["POST"])
def branding_strategy():
    data = request.json
    user_input = data.get("user_input", "")
    report = generate_branding_strategy(user_input)
    store_report(data["user_id"], report)
    return jsonify({"branding_report": report})

if __name__ == "__main__":
    app.run(debug=True)
