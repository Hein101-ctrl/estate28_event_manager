import frappe

DOCTYPE = "Estate 28 Event"

def _get_columns():
    return {f.fieldname for f in frappe.get_meta(DOCTYPE).fields if getattr(f, "fieldname", None)}

def _pick(*names):
    cols = _get_columns()
    for n in names:
        if n in cols:
            return n
    return None

def execute(filters=None):
    photographer = _pick("photographer")
    client = _pick("client_name")
    event_date = _pick("event_date")
    venue = _pick("venue_area")
    status = _pick("internal_status", "status")

    columns = [
        {"label": "Photographer", "fieldname": "photographer", "fieldtype": "Data", "width": 180},
        {"label": "Event Date", "fieldname": "event_date", "fieldtype": "Date", "width": 110},
        {"label": "Client Name", "fieldname": "client_name", "fieldtype": "Data", "width": 220},
        {"label": "Venue Area", "fieldname": "venue_area", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

    if not event_date:
        return columns, []

    data = frappe.db.sql(f"""
        SELECT
            {f"`{photographer}`" if photographer else "'Unassigned'"} AS photographer,
            `{event_date}` AS event_date,
            {f"`{client}`" if client else "name"} AS client_name,
            {f"`{venue}`" if venue else "''"} AS venue_area,
            {f"`{status}`" if status else "''"} AS status
        FROM `tab{DOCTYPE}`
        WHERE `{event_date}` >= CURDATE()
        ORDER BY photographer ASC, `{event_date}` ASC
    """, as_dict=True)
    return columns, data
