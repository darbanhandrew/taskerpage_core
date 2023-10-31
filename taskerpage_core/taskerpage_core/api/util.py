import frappe


@frappe.whitelist()
def get_possible_transitions(current_state, doctype):
    workflow_name = frappe.get_value(
        "Workflow", {"document_type": doctype}, "name")
    if not workflow_name:
        return []

    transitions = frappe.get_all("Workflow Transition", filters={
        "parent": workflow_name,
        "state": current_state
    }, fields=["state", "allowed", "next_state", "action"])

    return transitions
