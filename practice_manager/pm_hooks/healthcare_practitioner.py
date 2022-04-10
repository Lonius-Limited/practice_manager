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
	message ="""<p>Dear <b style='color:green'>{}</b> <b style='color:green'>{}</b> <br/>
			A practitioner account has been successfully set up for you.\nYou will be able to set your login password via the provided email address:  <b style='color:blue'>{}. </p> 
			<p>Once you have logged in, click on the 'Practice' Menu on the left hand of the screen. You will be presented with the following menu buttons and actions you can do:
			<br/><ul>
			<li><b style='color:green'>New Consult Ledger</b> - You will be able to record your consults and bills done here</li>
			<li><b style='color:green'>Consult Ledgers</b> - Here is your list of all bills you have recorded</li>
			<li><b style='color:green'>Receivables </b>- This is a report tracking your accounts receivables aged for each hospital/facility that owes you.</li>
			<li><b style='color:green'>Receivables Summary </b>- Just like above but a little summarized</li>
			<li><b style='color:green'>Ledger Summary </b>- A report of the opening balances, total billed, total paid and closing balances for each hospital/facility.</li>
			<li><b style='color:green'>Record Payment </b>- You will be able to record every payment received from a hospital/facility and you can pull unpaid invoices against which the payments will be allocated automatically.</li>
			<li><b style='color:green'>Payments </b>- This is a list of all payment details you have recorded from all the facilities.</li>
			<li><b style='color:green'>Patient List </b>- The is the Patient Master List. You can add all your patients here. A number of details can be added for each patient.</li>
			<li><b style='color:green'>Facility List </b>- This is the Facility Master List. Ideally all level 3 and above Facilities in the country have been added. Contact us if you feel a facility is missing.</li>
			<li><b style='color:green'>Patient Encounters </b>- A list of all patient encounters you have recorded.</li>
			<li><b style='color:green'>New Patient Encounter </b>- It will allow you to record encounter details about a patient. You can record their history, common presenting complaints, order labs, radiology and prescriptions among other things.</li>
			</ul>
			</p>
			<p>We hope this can help you quickly get you started on Lonius Practice Manager. Enjoy the instant benefits of never staying in the dark about your Practice.<br/> If you have any questions contact us via the email: info@lonius.co.ke.
			</p><br/><br/>""".format(doc.get('first_name').title(),doc.get('last_name').title(),doc.get('email_address').lower())
	# frappe.msgprint(f"{message}")
	alert_practitioner(doc,message)
def alert_practitioner(doc, message):
	"""send email with payment link"""
	email_args = {
		"recipients": doc.get("email_address"),
		# "sender": None,
		"subject": 'Welcome to Practice Manager!',
		"message": message,
		"now": True,
		"attachments": [frappe.attach_print(doc.doctype, doc.name,
			file_name=doc.name)]}
	frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
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
	user.append('roles',dict(role='Accounts Manager'))
	user.append('roles',dict(role='Accounts User'))
	user.append('roles',dict(role='Dashboard Manager'))
	user.append('roles',dict(role='Sales Master Manager'))
	user.append('roles',dict(role='Sales Manager'))
	user.append('roles',dict(role='Sales User'))
	
	#BLOCK ALL MODULES THAT THEY DON'T NEED ACCESS TO
	from frappe.config import get_modules_from_all_apps
	user.set('block_modules', [])
	allowed_modules = ['Workflow', 'Desk', 'Printing', 'Healthcare', 'Practice Manager']
	for m in get_modules_from_all_apps():
		if m.get("module_name") not in allowed_modules:
			user.append('block_modules', {
				'module': m.get("module_name") 
			})
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
