import frappe
import json
@frappe.whitelist()
def cash():
    user = frappe.session.user
 
    result = frappe.db.sql(f"select SUM(amount) as amount from `tabConsult Ledger` where owner ='{user}' ", as_dict = 1)
    invoices = result[0].get('amount') or 0
    
    result = frappe.db.sql(f"select COUNT( DISTINCT facility) as amount from `tabConsult Ledger` where owner ='{user}' ", as_dict = 1)
    facilities = result[0].get('amount') or 0

    user = frappe.session.user
    result = frappe.db.sql(f"select SUM(paid_amount) as amount from `tabPayment Entry` where owner ='{user}' ", as_dict=1)
    payments = result[0].get('amount') or 0

    result = frappe.db.sql(f"select COUNT(name) as amount from `tabPatient` where owner ='{user}'", as_dict = 1)
    patients= result[0].get('amount') or 0

    result = frappe.db.sql(f"select COUNT(name) as amount from `tabPatient Encounter` where owner ='{user}' ", as_dict = 1)
    patient_encounters = result[0].get('amount') or 0

    return dict(facilities = facilities, invoices=invoices, payments = payments, patients = patients, patient_encounters = patient_encounters)pyalo

@frappe.whitelist()
def submit(payload):
    data = json.loads(payload)
    doctype = data.get("doctype")
    name = data.get("name")
    doc  = frappe.get_doct(doctype, name)
    doc.submit()
    
@frappe.whitelist()
def get_company()
    return frappe.defaults.get_user_default('company')
