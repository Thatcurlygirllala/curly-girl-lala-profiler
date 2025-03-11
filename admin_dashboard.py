class AdminDashboard:
    def __init__(self):
        self.reports = {}

    def generate_client_report(self, client_id, user_input):
        report = generate_branding_strategy(user_input)
        self.reports[client_id] = report
        return report

    def resend_client_report(self, client_id):
        return self.reports.get(client_id, "No report found.")

    def list_all_reports(self):
        return self.reports
