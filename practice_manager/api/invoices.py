import frappe
import datetime
from frappe import _, msgprint
from frappe.utils import flt, get_defaults
from frappe.utils.data import now_datetime

def open_invoice_exists(customer, patient):
	invoices = frappe.get_list('Sales Invoice', filters={
		'customer': customer,
		'patient': patient
	}, fields=['name', 'status'],  order_by='creation desc')
	if len(invoices) > 0:
		return invoices[0]
	return False

def invoice_consult(consult):
	customer = consult.get('facility')
	patient = consult.get('patient')
	company = frappe.defaults.get_user_default("company")
	existing_invoice = open_invoice_exists(customer=customer, patient=patient)
	if consult.get('payer_type') == 'Cash Payer':
		narrative = consult.get('service_name') + ' - ' + consult.get('patient_name') + ' (' + consult.get('payer_type') + ')'
	else:
		narrative = consult.get('service_name') + ' - ' + consult.get('patient_name') + ' (' + consult.get('payer_type') + ' | ' + consult.get('insurance') + ')'
	if not existing_invoice or not existing_invoice.get('status') == 'Draft':
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"status": "Draft",
			"company": consult.get('company'),
			'due_date': datetime.date.today(),
			"currency": "KES",
			"customer": customer,
			"patient": patient,
			"generated_by": 'Practice Manager',
			"allocate_advances_automatically": 1
		})
		invoice.append('items', {
			"item_code": consult.get('service'),
			"description":  narrative,
			"qty": 1,
			"rate": consult.get('amount')
		})
		invoice.run_method('set_missing_values')
		invoice.insert(ignore_permissions=True)
	else:
		invoice = frappe.get_doc('Sales Invoice', existing_invoice.get('name'))
		invoice.due_date = datetime.date.today()
		invoice.payment_schedule = {}
		invoice.append('items', {
			"item_code": consult.get('service'),
			"description": narrative,
			"qty": 1,
			"rate": consult.get('amount')
		})
		invoice.run_method('set_missing_values')
		invoice.save(ignore_permissions=True)
	if consult.get('encounter_type') == 'Outpatient':
		invoice.submit()
	frappe.msgprint(
		_("The facility {} has been invoiced for the service.".format(customer)),)
	return invoice