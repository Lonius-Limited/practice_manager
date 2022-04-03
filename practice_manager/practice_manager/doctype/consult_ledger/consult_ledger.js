// Copyright (c) 2022, Lonius Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consult Ledger', {
	// refresh: function(frm) {

	// }
	service: function(frm) {
		frm.call('get_this_item_price', { facility: frm.doc.facility, service: frm.doc.service })
		.then(r => {
			if (r.message) {
				console.log('Price - ' +  r.message);
				frm.set_value('amount',  r.message)
			}
		})
	}
});
