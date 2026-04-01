import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, today


DEFAULT_ITEM_CODE = "Event Booking"


class Estate28Event(Document):
    def autoname(self):
        if self.client_name and self.event_date:
            self.name = f"{self.client_name} - {self.event_date}"

    def validate(self):
        self.set_title()
        self.set_due_dates()
        self.set_balance_due()

    def set_title(self):
        if self.client_name and self.event_date:
            self.event_title = f"{self.client_name} - {self.event_date}"

    def set_balance_due(self):
        package_amount = self.package_amount or 0
        amount_paid = self.amount_paid or 0
        self.balance_due = max(package_amount - amount_paid, 0)

    def set_due_dates(self):
        if self.event_date:
            if not self.final_payment_due_date:
                self.final_payment_due_date = add_days(self.event_date, -21)
            if not self.final_numbers_due_date:
                self.final_numbers_due_date = add_days(self.event_date, -28)


@frappe.whitelist()
def create_customer_from_event(docname):
    doc = frappe.get_doc("Estate 28 Event", docname)

    if doc.customer:
        return doc.customer

    existing = frappe.db.get_value("Customer", {"customer_name": doc.client_name}, "name")
    if existing:
        doc.db_set("customer", existing)
        return existing

    customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": doc.client_name,
        "customer_type": "Individual",
        "customer_group": "All Customer Groups",
        "territory": "All Territories",
        "mobile_no": doc.client_phone or None,
        "email_id": doc.client_email or None
    })
    customer.insert(ignore_permissions=True)

    doc.db_set("customer", customer.name)
    return customer.name


@frappe.whitelist()
def create_sales_invoice_from_event(docname):
    doc = frappe.get_doc("Estate 28 Event", docname)

    if doc.sales_invoice:
        frappe.throw(f"Sales Invoice already exists: {doc.sales_invoice}")

    customer_name = create_customer_from_event(docname)

    rate = doc.package_amount or 0
    if not rate:
        frappe.throw("Package amount is required before creating a Sales Invoice.")

    posting_date = getdate(today())

    candidate_due_date = None
    if doc.final_payment_due_date:
        candidate_due_date = getdate(doc.final_payment_due_date)
    elif doc.event_date:
        candidate_due_date = getdate(doc.event_date)

    if candidate_due_date and candidate_due_date >= posting_date:
        due_date = candidate_due_date
    else:
        due_date = posting_date

    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": customer_name,
        "posting_date": posting_date,
        "due_date": due_date,
        "remarks": f"Generated from Estate 28 Event {doc.name}",
        "items": [
            {
                "item_code": DEFAULT_ITEM_CODE,
                "item_name": "Event Booking",
                "description": f"{doc.event_type or 'Event'} booking for {doc.client_name} on {doc.event_date}",
                "qty": 1,
                "rate": rate
            }
        ]
    })
    invoice.insert(ignore_permissions=True)

    doc.db_set("sales_invoice", invoice.name)
    return invoice.name
