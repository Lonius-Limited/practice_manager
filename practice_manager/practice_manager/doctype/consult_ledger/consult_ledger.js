// Copyright (c) 2022, Lonius Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consult Ledger', {
	refresh: function(frm) {
		if (frm.doc.encounter_type == 'Inpatient' && frm.doc.docstatus == 1) {
			frm.add_custom_button('End Encounter/Discharge', () => {
				frm.call('end_encounter', {}).then(r => {
					frm.remove_custom_button('End Encounter/Discharge');
				})
			})
		}

		/* if (!frm.is_new()) {
			frm.call('get_associated_invoice', {})
			.then(r => {
				if (r.message) {
					console.log('Invoice - ' +  JSON.stringify(r.message));
					var message = "Invoice: <a target='_blank' href='/app/sales-invoice/" + r.message.name + "'> " + r.message.name + "</a> - Amount: " + r.message.grand_total;
					frm.dashboard.add_section(message);
					frm.dashboard.show();
				}
			})
		} */
		if (frm.doc.invoice) {
			// console.log('Invoice: ' + frm.doc.invoice)
			frm.call('get_invoice_total', {})
			.then(r => {
				console.log('Invoice Total: ' + r.message.grand_total)
				var message = "Invoice: <a target='_blank' href='/app/sales-invoice/" + frm.doc.invoice + "'> " + frm.doc.invoice + "</a> - Total Invoiced: " + r.message.grand_total;
				frm.dashboard.add_section(message);
				frm.dashboard.show();
				if (r.message.docstatus == 1) {
					frm.remove_custom_button('End Encounter/Discharge');
				}
			})
		}
	},
	onload: function(frm) {
		if (frm.doc.docstatus == 0) {
			frm.set_intro('An invoice is generated automatically on submit of this document');
		}
		frm.set_query('facility', () => {
			return {
				filters: {
					industry: 'Healthcare'
				}
			}
		}),
		frm.set_query('insurance', () => {
			return {
				filters: {
					industry: 'Insurance'
				}
			}
		})
	},
	service: function(frm) {
		frm.call('get_this_item_price', { facility: frm.doc.facility, service: frm.doc.service, insurance: frm.doc.insurance })
		.then(r => {
			if (r.message) {
				console.log('Price - ' +  r.message);
				frm.set_value('amount',  r.message)
			}
		})
	},
	encounter_type: function(frm) {
		if (frm.doc.encounter_type == 'Inpatient' && frm.doc.docstatus == 1) {
			frm.add_custom_button('End Encounter/Discharge', () => {
				frm.call('end_encounter', {}).then(r => {
					frm.remove_custom_button('End Encounter/Discharge');
				})
			})
		} else {
			frm.remove_custom_button('End Encounter/Discharge');
		}
	}
});
