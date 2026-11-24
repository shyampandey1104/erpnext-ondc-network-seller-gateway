# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "ondc_seller_gateway"
app_title = "Erpnext Ondc Network Seller Gateway"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Ondc Network Seller Gateway - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/ondc_seller_gateway/css/ondc_seller_gateway.bundle.css"
app_include_js = "/assets/ondc_seller_gateway/js/ondc_seller_gateway.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Ondc Network Seller Gateway Entry": {
        "validate": "ondc_seller_gateway.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "ondc_seller_gateway.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "ondc_seller_gateway.tasks.hourly_sync"
    ],
    "daily": [
        "ondc_seller_gateway.tasks.daily_reconciliation"
    ],
    "weekly": [
        "ondc_seller_gateway.tasks.weekly_digest"
    ]
}
