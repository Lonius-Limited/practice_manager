# Copyright (c) 2022, Lonius Limited and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from practice_manager.api.invoices import invoice_consult

class ConsultLedger(Document):
	def on_submit(self):
		invoice_consult(self)