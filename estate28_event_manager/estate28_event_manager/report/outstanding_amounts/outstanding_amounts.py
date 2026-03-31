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
    total = _pick("total_amount", "package_amount")
    paid = _pick("amount_paid")
    balance = _pick("balance_due")
    final_payment = _pick("final_payment_date", "final_payment_due_date")
    status = _pick("internal_status", "status")

    columns = [
        {"label": "Client Name", "fieldname": "client_name", "fieldtype": "Data", "width": 220},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Amount Paid", "fieldname": "amount_paid", "fieldtype": "Currency", "width": 120},
        {"label": "Balance Due", "fieldname": "balance_due", "fieldtype": "Currency", "width": 120},
        {"label": "Final Payment Date", "fieldname": "final_payment_date", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

    if not client or not balance:
        return columns, []

    data = frappe.db.sql(f"""
        SELECT
            `{client}` AS client_name,
            {f"`{total}`" if total else "0"} AS total_amount,
            {f"`{paid}`" if paid else "0"} AS amount_paid,
            `{balance}` AS balance_due,
            {f"`{final_payment}`" if final_payment else "NULL"} AS final_payment_date,
            {f"`{status}`" if status else "''"} AS status
        FROM `tab{DOCTYPE}`
        WHERE IFNULL(`{balance}`, 0) > 0
        ORDER BY IFNULL(`{balance}`, 0) DESC
    """, as_dict=True)
    return columns, data
