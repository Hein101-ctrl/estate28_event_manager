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
    status = _pick("internal_status", "status")
    columns = [
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 180},
        {"label": "Wedding Count", "fieldname": "wedding_count", "fieldtype": "Int", "width": 140},
    ]

    if not status:
        return columns, []

    data = frappe.db.sql(f"""
        SELECT `{status}` AS status, COUNT(*) AS wedding_count
        FROM `tab{DOCTYPE}`
        GROUP BY `{status}`
        ORDER BY wedding_count DESC, `{status}` ASC
    """, as_dict=True)
    return columns, data
