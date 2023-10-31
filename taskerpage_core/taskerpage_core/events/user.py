import frappe
import uuid

def assign_member_number(doc, method):
    # Check if the member number is not already assigned
    if not doc.member_number:
        # Generate the member number
        # This is just a simple example; you can have a more complex logic
        doc.member_number = generate_unique_member_number()


def generate_unique_member_number():
    return str(uuid.uuid4())