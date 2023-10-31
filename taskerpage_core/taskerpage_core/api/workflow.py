import frappe
from frappe.model.workflow import apply_workflow, get_workflow_name
from chat.api.message import send


def get_message_for_action(action_name, refrence_doctype, refrence_docname):
    # Fetch the corresponding template for the action
    template_data = frappe.get_value(
        "App Message Template", {"action": action_name}, "message_template")

    if not template_data:
        frappe.throw(
            ("No message template found for action: {0}").format(action_name))

    # Return the formatted message
    return template_data.format(refrence_doctype, refrence_docname)


@frappe.whitelist()
def process_action(doctype, docname, action, refrence_doctype, refrence_docname):
    try:
        # Fetching the document based on provided doctype and docname
        target_doc = frappe.get_doc(doctype, docname)

        # If the document has fields 'refrence_doctype' and 'refrence_docname',
        # set them to the values provided.
        # if 'refrence_doctype' in kwargs and 'refrence_docname' in kwargs:
        #     if hasattr(target_doc, 'refrence_doctype') and hasattr(target_doc, 'refrence_docname'):
        #         target_doc.refrence_doctype = kwargs['refrence_doctype']
        #         target_doc.refrence_docname = kwargs['refrence_docname']
        #         target_doc.save()

        workflow_name = get_workflow_name(target_doc.doctype)

        # Check if the action is applicable to the current state of the document
        if workflow_name:
            # Apply the workflow action to the document
            apply_workflow(target_doc, action)
            if doctype == "Chat Message":
                content = get_message_for_action(
                    action, refrence_doctype, refrence_docname)
                user = frappe.session.user
                email = frappe.get_value("User", user, "email")
                room = target_doc.room
                send(
                    content=content,
                    user=user,
                    room=room,
                    email=email,
                    reference_doctype=refrence_doctype,
                    reference_docname=refrence_docname
                )
            if doctype == "Chat Room":
                content = get_message_for_action(
                    action, refrence_doctype, refrence_docname)
                user = frappe.session.user
                email = frappe.get_value("User", user, "email")
                room = target_doc.name
                send(
                    content=content,
                    user=user,
                    room=room,
                    email=email,
                    reference_doctype=refrence_doctype,
                    reference_docname=refrence_docname
                )

            return {
                "status": "success",
                "message": f"Action '{action}' has been applied successfully!"
            }
        else:
            return {
                "status": "error",
                "message": f"No workflow found for Doctype '{target_doc.doctype}'."
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
