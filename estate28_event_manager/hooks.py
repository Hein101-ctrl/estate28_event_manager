app_name = "estate28_event_manager"
app_title = "Estate28 Event Manager"
app_publisher = "Estate28"
app_description = "Wedding and event planning app for Estate28"
app_email = "info@estate28.co.za"
app_license = "MIT"

# Keep the live DocType schema exactly as v3.
# v4 clean only adds workspace, dashboard, reports and helper API.
fixtures = [
    {
        "doctype": "Workspace",
        "filters": [["name", "=", "Estate28 Event Manager"]]
    }
]

doctype_js = {
    "Estate 28 Event": "public/js/estate_28_event.js"
}
