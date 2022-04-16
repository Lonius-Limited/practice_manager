# Copyright (c) 2022, Lonius Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from practice_manager.api.invoices import invoice_consult, open_invoice_exists
from practice_manager.api.prices import update_item_price, get_item_price

class ConsultLedger(Document):
	def on_submit(self):
		invoice = invoice_consult(self)
		frappe.db.set_value('Consult Ledger', self.name, 'invoice', invoice.get('name'))
		update_item_price(self.facility, self.service, self.amount, self.insurance)

	def on_update(self):
		frappe.db.set_value('Patient', self.patient, 'customer', self.facility)

	@frappe.whitelist()
	def get_associated_invoice(self):
		existing_invoice = open_invoice_exists(self.facility, self.patient)
		return frappe.get_doc('Sales Invoice', existing_invoice.get('name')) if existing_invoice else False
	
	@frappe.whitelist()
	def get_this_item_price(self, facility, service, insurance=None):
		return get_item_price(facility, service, insurance)

	@frappe.whitelist()
	def end_encounter(self):
		the_invoice = self.get_associated_invoice()
		if the_invoice:
			the_invoice.submit()
			frappe.msgprint('The patient encounter has been ended and the invoice finalized')
	
	@frappe.whitelist()
	def get_invoice_total(self):
		return frappe.get_doc('Sales Invoice', self.invoice)