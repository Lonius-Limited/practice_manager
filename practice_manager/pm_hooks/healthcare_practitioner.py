import frappe
import string, random
from frappe.core.doctype.user_permission.user_permission import clear_user_permissions
def get_company_id():
	payload = string.ascii_uppercase + "1234567890"
	abbr1 = random.choices(payload, k=5)
	return "".join(abbr1)
def link_user_and_company(doc, state):
	company = make_company(doc)
	user = make_and_link_user(doc)
	add_restrictions(doc, user, company)
	doc.set('user_id', user.get('name'))
	doc.save(ignore_permissions=True)
	message = "<p>Dear <b style='color:green'>{}</b> <b style='color:green'>{}</b>, your Practice Manager account has been successfully set up. User credentials have been sent to you on your official email: <b style='color:blue'>{}</b> </p>".format(doc.get('first_name').upper(),doc.get('last_name').title(),doc.get('email_address').lower())
	frappe.msgprint(f"{message}")
	alert_practitioner(doc,message)
def alert_practitioner(doc, message):
	"""send email with payment link"""
		email_args = {
			"recipients": doc.get("email_address"),
			# "sender": None,
			"subject": 'Welcome to Practice Manager!',
			"message": message,
			"now": True,
			"attachments": [frappe.attach_print(self.reference_doctype, self.reference_name,
				file_name=self.reference_name, print_format=self.print_format)]}
		enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
def make_company(doc):
	pc = frappe.get_all(
		"Company",
		filters=dict(is_group=1, parent_company=""),
		fields=["*"],
		order_by="creation DESC",
		page_length=1,
	)
	if not pc:
		frappe.throw(
			"Sorry, a root company is not set up in the company tree. Requirements : Is Group=1,Parent Company =''"
		)
	parent_company = pc[0]
	args = dict(
		doctype="Company",
		company_name=doc.get("name"),
		parent_company=parent_company.get("name"),
		is_group=0,
		abbr=get_company_id(),
		default_currency=parent_company.get("default_currency"),
		country=parent_company.get("country"),
	)
	company = frappe.get_doc(args).save(ignore_permissions=1)
	return company


def make_and_link_user(doc):
	args = {
		"doctype": "User",
		"send_welcome_email": 1,
		"email": doc.get('email_address'),
		"first_name": doc.get("first_name"),
		"user_type": "System User",
	}
	user = frappe.get_doc(args)

	user.append('roles',dict(role='Physician'))
	# user.role_profile_name = 'Vendor Profile'
	user.save(ignore_permissions=True)
	return user


def add_restrictions(doc, user, company):
	clear_user_permissions(user, "Company")
	frappe.get_doc(
		dict(
			doctype="User Permission",
			user=user.get('name'),
			allow="Company",
			for_value=company.get('name'),
			apply_to_all_doctypes=1,
			# applicable_for="Material Request",
		)
	).insert(ignore_permissions=True)
