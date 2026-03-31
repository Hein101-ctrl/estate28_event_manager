import frappe
from frappe.model.document import Document

class Estate28Event(Document):
    def validate(self):
        if self.total_guests is not None and self.total_guests < 0:
            frappe.throw("Total Guests cannot be negative.")
        if self.kids_count is not None and self.kids_count < 0:
            frappe.throw("Kids Count cannot be negative.")
        if self.service_providers_count is not None and self.service_providers_count < 0:
            frappe.throw("Service Providers Count cannot be negative.")
        if self.wheelchair_guests is not None and self.wheelchair_guests < 0:
            frappe.throw("Wheelchair Guests cannot be negative.")
