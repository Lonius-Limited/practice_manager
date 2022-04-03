# Copyright (c) 2022, Lonius Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from practice_manager.api.invoices import invoice_consult
from practice_manager.api.prices import update_item_price, get_item_price

class ConsultLedger(Document):
	def on_submit(self):
		invoice_consult(self)
		update_item_price(self.facility, self.service, self.amount)
	
	@frappe.whitelist()
	def get_this_item_price(self, facility, service):
		return get_item_price(facility, service)