import frappe
import datetime
from frappe import _, msgprint
from frappe.utils import flt, get_defaults
from frappe.utils.data import now_datetime

import lonius_health
# CAN WE PLEASE AVOID HARD CODING ANYTHING! "Lonius Limited"


def open_invoice_exists(customer):
	invoices = frappe.get_list('Sales Invoice', filters={
		'status': 'Draft',
		'customer': customer
	})
	if len(invoices) > 0:
		return invoices[0]
	return False

def invoice_consult(consult):
	customer = consult.get('facility')
	company = frappe.defaults.get_user_default("company")
	existing_invoice = open_invoice_exists(customer=customer)
	if not existing_invoice:
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"status": "Draft",
			"company": company,
			'due_date': datetime.date.today(),
			"currency": "KES",
			"customer": customer,
			"allocate_advances_automatically": 1
		})
		invoice.append('items', {
			"item_code": consult.get('service'),
			"description": consult.get('service_name') + ' - ' + consult.get('patient_name'),
			"qty": 1,
			"rate": consult.get('amount')
		})
		invoice.run_method('set_missing_values')
		invoice.insert()
	else:
		invoice = frappe.get_doc('Sales Invoice', existing_invoice.get('name'))
		invoice.append('items', {
			"item_code": consult.get('service'),
			"description": consult.get('service_name') + ' - ' + consult.get('patient_name'),
			"qty": 1,
			"rate": consult.get('amount')
		})
		invoice.run_method('set_missing_values')
		invoice.save()
	
	frappe.msgprint(
		_("The facility {} has been invoiced for the service.".format(customer)),)
	return