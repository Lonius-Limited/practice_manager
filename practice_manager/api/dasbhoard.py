import frappe
@frappe.whitelist()
def cash():
    user = frappe.session.user
    invoices = 0
    result = frappe.db.sql(f"select SUM(amount) as amount from `tabConsult Ledger` where owner ='{user}' ", as_dict = 1)
    invoices = result[0].get('amount')

    user = frappe.session.user
    result = frappe.db.sql(f"select SUM(paid_amount) as amount from `tabPayment Entry` where owner ='{user}' ", as_dict=1)
    payments = result[0].get('amount') or 0

    result = frappe.db.sql(f"select COUNT(name) as amount from `tabPatient` where owner ='{user}'", as_dict = 1)
    patients= result[0].get('amount') or 0

    result = frappe.db.sql(f"select SUM(name) as amount from `tabPatient Encounter` where owner ='{user}' ", as_dict = 1)
    patient_encounters = result[0].get('amount') or 0

    return dict(invoices=invoices, payments = payments, patients = patients, patient_encounters = patient_encounters)