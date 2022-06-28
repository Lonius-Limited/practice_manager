frappe.form.link_formatters['Customer'] = function(value, doc) {
    console.log('VALUE: ' + value);
    if(doc.customer_name && doc.customer_name !== value) {
        return value + ': ' + doc.customer_name;
    } else {
        return value;
    }
}