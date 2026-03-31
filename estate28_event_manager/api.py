import frappe
from frappe import _

DOCTYPE = "Estate 28 Event"

def _get_columns():
    try:
        return {c.get("fieldname") for c in frappe.get_meta(DOCTYPE).fields if c.get("fieldname")}
    except Exception:
        return set()

def _pick(*names):
    cols = _get_columns()
    for n in names:
        if n in cols:
            return n
    return None

def _q(fieldname, fallback="''"):
    if fieldname:
        return f"`{fieldname}`"
    return fallback

@frappe.whitelist()
def get_dashboard_summary():
    total_field = _pick("total_amount", "package_amount")
    paid_field = _pick("amount_paid")
    balance_field = _pick("balance_due")
    status_field = _pick("internal_status", "status")
    event_date_field = _pick("event_date")
    final_payment_field = _pick("final_payment_date", "final_payment_due_date")

    summary = {
        "total_weddings": 0,
        "upcoming_30_days": 0,
        "outstanding_total": 0,
        "overdue_payments": 0,
        "booked_count": 0,
    }

    if not event_date_field:
        return summary

    total_row = frappe.db.sql(f"""
        SELECT COUNT(*) AS total_weddings
        FROM `tab{DOCTYPE}`
    """, as_dict=True)[0]
    summary["total_weddings"] = total_row.get("total_weddings", 0) or 0

    upcoming_row = frappe.db.sql(f"""
        SELECT COUNT(*) AS cnt
        FROM `tab{DOCTYPE}`
        WHERE `{event_date_field}` BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """, as_dict=True)[0]
    summary["upcoming_30_days"] = upcoming_row.get("cnt", 0) or 0

    if balance_field:
        bal_row = frappe.db.sql(f"""
            SELECT COALESCE(SUM(IFNULL(`{balance_field}`, 0)), 0) AS total
            FROM `tab{DOCTYPE}`
        """, as_dict=True)[0]
        summary["outstanding_total"] = float(bal_row.get("total", 0) or 0)

    if final_payment_field and balance_field:
        overdue_row = frappe.db.sql(f"""
            SELECT COUNT(*) AS cnt
            FROM `tab{DOCTYPE}`
            WHERE `{final_payment_field}` IS NOT NULL
              AND `{final_payment_field}` < CURDATE()
              AND IFNULL(`{balance_field}`, 0) > 0
        """, as_dict=True)[0]
        summary["overdue_payments"] = overdue_row.get("cnt", 0) or 0

    if status_field:
        booked_row = frappe.db.sql(f"""
            SELECT COUNT(*) AS cnt
            FROM `tab{DOCTYPE}`
            WHERE `{status_field}` IN ('Booked', 'Planning', 'Final Numbers')
        """, as_dict=True)[0]
        summary["booked_count"] = booked_row.get("cnt", 0) or 0

    return summary

@frappe.whitelist()
def get_upcoming_weddings(limit=10):
    limit = int(limit or 10)
    client_field = _pick("client_name")
    date_field = _pick("event_date")
    package_field = _pick("package_quote", "package_type")
    photographer_field = _pick("photographer")
    dj_field = _pick("dj")
    balance_field = _pick("balance_due")
    final_payment_field = _pick("final_payment_date", "final_payment_due_date")
    status_field = _pick("internal_status", "status")

    if not date_field or not client_field:
        return []

    rows = frappe.db.sql(f"""
        SELECT
            name,
            { _q(client_field) } AS client_name,
            `{date_field}` AS event_date,
            { _q(package_field) } AS package_label,
            { _q(photographer_field) } AS photographer,
            { _q(dj_field) } AS dj,
            { _q(balance_field, "0") } AS balance_due,
            { _q(final_payment_field) } AS final_payment_date,
            { _q(status_field) } AS internal_status
        FROM `tab{DOCTYPE}`
        WHERE `{date_field}` >= CURDATE()
        ORDER BY `{date_field}` ASC
        LIMIT %(limit)s
    """, {"limit": limit}, as_dict=True)
    return rows

@frappe.whitelist()
def get_outstanding_amounts(limit=10):
    limit = int(limit or 10)
    client_field = _pick("client_name")
    total_field = _pick("total_amount", "package_amount")
    paid_field = _pick("amount_paid")
    balance_field = _pick("balance_due")
    final_payment_field = _pick("final_payment_date", "final_payment_due_date")
    date_field = _pick("event_date")

    if not client_field or not balance_field:
        return []

    rows = frappe.db.sql(f"""
        SELECT
            name,
            { _q(client_field) } AS client_name,
            { _q(total_field, "0") } AS total_amount,
            { _q(paid_field, "0") } AS amount_paid,
            `{balance_field}` AS balance_due,
            { _q(final_payment_field) } AS final_payment_date,
            { _q(date_field) } AS event_date
        FROM `tab{DOCTYPE}`
        WHERE IFNULL(`{balance_field}`, 0) > 0
        ORDER BY IFNULL(`{balance_field}`, 0) DESC, { _q(final_payment_field, "CURDATE()") } ASC
        LIMIT %(limit)s
    """, {"limit": limit}, as_dict=True)
    return rows

@frappe.whitelist()
def get_photographer_cards():
    photographer_field = _pick("photographer")
    client_field = _pick("client_name")
    date_field = _pick("event_date")
    balance_field = _pick("balance_due")

    if not photographer_field or not date_field:
        return []

    rows = frappe.db.sql(f"""
        SELECT
            IFNULL(NULLIF({ _q(photographer_field) }, ''), 'Unassigned') AS photographer,
            COUNT(*) AS upcoming_weddings,
            MIN(`{date_field}`) AS next_wedding_date,
            SUBSTRING_INDEX(
                GROUP_CONCAT({ _q(client_field, "'Unknown'") } ORDER BY `{date_field}` ASC SEPARATOR '||'),
                '||', 1
            ) AS next_client,
            COALESCE(SUM(IFNULL({ _q(balance_field, "0") }, 0)), 0) AS outstanding_total
        FROM `tab{DOCTYPE}`
        WHERE `{date_field}` >= CURDATE()
        GROUP BY IFNULL(NULLIF({ _q(photographer_field) }, ''), 'Unassigned')
        ORDER BY next_wedding_date ASC, photographer ASC
    """, as_dict=True)
    return rows
