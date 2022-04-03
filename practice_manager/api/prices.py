import frappe
import datetime
from frappe import _, msgprint
from frappe.utils import flt, get_defaults
from frappe.utils.data import now_datetime

def get_pricelist_for_customer(customer):
	if frappe.db.exists({"doctype": "Price List", "price_list_name": customer}):
		return frappe.db.get_list('Price List',
			filters={
				'price_list_name': customer
			})[0].get('name')
	else:
		doc = frappe.get_doc({
			'doctype': 'Price List',
			'currency': get_defaults().get('currency'),
			'price_list_name': customer,
			'selling': 1
		}).insert()
		return customer

def update_item_price(customer, item_code, rate):
	currency = get_defaults().get('currency')
	price_list = get_pricelist_for_customer(customer)
	item_price = frappe.db.get_value('Item Price',
		{'item_code': item_code, 'price_list': price_list, 'currency': currency},
		['name', 'price_list_rate'], as_dict=1)
	if item_price and item_price.name:
		frappe.db.set_value('Item Price', item_price.name, "price_list_rate", rate)
	else:
		item_price = frappe.get_doc({
			"doctype": "Item Price",
			"price_list": price_list,
			"item_code": item_code,
			"currency": currency,
			"price_list_rate": rate
		})
		item_price.insert()

def get_item_price(customer, item_code):
	currency = get_defaults().get('currency')
	price_list = get_pricelist_for_customer(customer)
	item_price = frappe.db.get_value('Item Price',
		{'item_code': item_code, 'price_list': price_list, 'currency': currency},
		['name', 'price_list_rate'], as_dict=1)
	if item_price and item_price.name:
		return item_price.price_list_rate
	return 0.0