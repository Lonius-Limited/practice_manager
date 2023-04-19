import frappe
import json
from erpnext.accounts.doctype.payment_entry.payment_entry import get_outstanding_reference_documents
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

    return dict(facilities = facilities, invoices=invoices, payments = payments, patients = patients, patient_encounters = patient_encounters)

@frappe.whitelist()
def submit(payload):
    data = json.loads(payload)
    doctype = data.get("doctype")
    name = data.get("name")
    doc  = frappe.get_doct(doctype, name)
    doc.submit()
  

@frappe.whitelist()
def get_company(owner= None):
    user =  owner or frappe.session.user
    return  frappe.db.get_value("Healthcare Practitioner", dict(email_address=user), "hospital")

def update_invoice_company(doc, flag):
    doc.company = get_company()
    doc.debit_to = frappe.db.get_value("Company", doc.company, "default_receivable_account")
    
    
    

def payment_entry(doc, flag):
    customer = doc.party
    company = get_company()
    debit_to = frappe.db.get_value("Company", company, "default_receivable_account")
    data = {"company":company,
        "party_type":"Customer",
        "payment_type":"Receive",   
        "party":customer,
         "party_account":debit_to,
        "outstanding_amt_greater_than":0,
        "outstanding_amt_less_than":100000000000000,
        "allocate_payment_amount":1}
    items = get_outstanding_reference_documents(data)
    doc.references = items
    
    
