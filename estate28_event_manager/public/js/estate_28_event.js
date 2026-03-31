frappe.ui.form.on("Estate 28 Event", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Create Customer", function () {
                frappe.call({
                    method: "estate28_event_manager.estate28_event_manager.doctype.estate_28_event.estate_28_event.create_customer_from_event",
                    args: { docname: frm.doc.name },
                    freeze: true,
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint("Customer ready: " + r.message);
                            frm.reload_doc();
                        }
                    }
                });
            });

            frm.add_custom_button("Create Sales Invoice", function () {
                frappe.call({
                    method: "estate28_event_manager.estate28_event_manager.doctype.estate_28_event.estate_28_event.create_sales_invoice_from_event",
                    args: { docname: frm.doc.name },
                    freeze: true,
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint("Sales Invoice created: " + r.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    },

    event_date(frm) {
        if (frm.doc.event_date && !frm.doc.final_payment_due_date) {
            let event_date = frappe.datetime.str_to_obj(frm.doc.event_date);
            let payment_due = frappe.datetime.add_days(event_date, -21);
            let numbers_due = frappe.datetime.add_days(event_date, -28);
            frm.set_value("final_payment_due_date", frappe.datetime.obj_to_str(payment_due));
            frm.set_value("final_numbers_due_date", frappe.datetime.obj_to_str(numbers_due));
        }
    }
});
