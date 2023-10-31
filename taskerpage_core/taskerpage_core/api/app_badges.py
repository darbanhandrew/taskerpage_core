import frappe


@frappe.whitelist()
def update_customer_profile_badges(customer_profile, app_badge):
    app_badge_doc = frappe.get_doc("App Badge", app_badge)
    app_badge_conditions = app_badge_doc.badge_conditions

    # Fetch the customer profile doc only once
    customer_profile_doc = frappe.get_doc("Customer Profile", customer_profile)

    badge_met = False  # This variable will track if all badge conditions are met

    for app_badge_condition in app_badge_conditions:
        if app_badge_condition.type == "Has Value":
            if not getattr(customer_profile_doc, app_badge_condition.field_name):
                break  # if the condition is not met, break out of loop

        elif app_badge_condition.type == "Exist":
            linked_docs = frappe.get_last_doc(app_badge_condition.linked_doctype, filters={
                                              f'{app_badge_condition.field_name}': customer_profile})
            if not linked_docs:
                break  # if the condition is not met, break out of loop

        elif app_badge_condition.type == "Compare":
            if getattr(customer_profile_doc, app_badge_condition.field_name) != app_badge_condition.value_to_compare:
                break  # if the condition is not met, break out of loop
    else:
        badge_met = True  # if the loop completes without breaking, all conditions are met

    badge_name_format = f"Customer Profile-{customer_profile}-badges-{app_badge}"
    # Check if the badge exists in the child table
    existing_badge = frappe.db.exists('Customer Profile Badge', {
                                      'name': badge_name_format})

    if existing_badge:
        # Update the existing badge
        badge_doc = frappe.get_doc('Customer Profile Badge', existing_badge)
        badge_doc.enabled = 1 if badge_met else 0
        badge_doc.save()

    else:
        # Insert a new badge directly into the child table
        badge_doc = frappe.get_doc({
            'doctype': 'Customer Profile Badge',
            'name': badge_name_format,
            'parent': customer_profile,
            'parenttype': 'Customer Profile',
            # Assuming 'badges' is the fieldname of the child table in the Customer Profile doctype
            'parentfield': 'badges',
            'badge_name': app_badge,
            'enabled': 1 if badge_met else 0
        }).insert()

    frappe.db.commit()
    return badge_doc
