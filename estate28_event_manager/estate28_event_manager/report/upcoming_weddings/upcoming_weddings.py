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
    client = _pick("client_name")
    event_date = _pick("event_date")
    package = _pick("package_quote", "package_type")
    photographer = _pick("photographer")
    dj = _pick("dj")
    status = _pick("internal_status", "status")

    columns = [
        {"label": "Client Name", "fieldname": "client_name", "fieldtype": "Data", "width": 220},
        {"label": "Event Date", "fieldname": "event_date", "fieldtype": "Date", "width": 110},
        {"label": "Package", "fieldname": "package_label", "fieldtype": "Data", "width": 150},
        {"label": "Photographer", "fieldname": "photographer", "fieldtype": "Data", "width": 170},
        {"label": "DJ", "fieldname": "dj", "fieldtype": "Data", "width": 170},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
    ]

    if not client or not event_date:
        return columns, []

    data = frappe.db.sql(f"""
        SELECT
            `{client}` AS client_name,
            `{event_date}` AS event_date,
            {f"`{package}`" if package else "''"} AS package_label,
            {f"`{photographer}`" if photographer else "''"} AS photographer,
            {f"`{dj}`" if dj else "''"} AS dj,
            {f"`{status}`" if status else "''"} AS status
        FROM `tab{DOCTYPE}`
        WHERE `{event_date}` >= CURDATE()
        ORDER BY `{event_date}` ASC
    """, as_dict=True)
    return columns, data
