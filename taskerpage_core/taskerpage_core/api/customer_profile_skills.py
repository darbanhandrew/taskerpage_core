import frappe
from typing import List
import json


@frappe.whitelist()
def get_my_skill_categories(customer_profile=None):
    if not customer_profile:
        user = frappe.session.user
        if user == 'Guest' or not user:
            frappe.response["message"] = "you are not authorized"
            frappe.response["http_status_code"] = 400
            return
        customer_profile_doc = frappe.get_last_doc(
            "Customer Profile", filters={"user": user})
        if not customer_profile_doc:
            frappe.response["message"] = "Customer Profile does not exist for user, contact support"
            return
    else:
        customer_profile_doc = frappe.get_doc(
            "Customer Profile", customer_profile)
    customer_profile_skills = frappe.get_list("Customer Profile Skills", fields=[
                                              "name", "skill_category_name"], filters=[["customer_profile", "=", customer_profile_doc.name]])
    # Using a dictionary to ensure unique skill_category_name
    unique_skills = {}
    for skill in customer_profile_skills:
        skill_category = skill.get("skill_category_name")
        if skill_category not in unique_skills:
            unique_skills[skill_category] = skill.get("name")

    # Convert dictionary to a list of dicts for the result
    result = [{"name": name, "skill_category_name": skill_category}
              for skill_category, name in unique_skills.items()]
    frappe.response["message"] = result
    return


@frappe.whitelist()
def sync_skill_categories():
    # Fetching the existing skills associated with the customer profile
    new_skills_list_str = frappe.form_dict.get('new_skills_list')
    customer_profile_name = frappe.form_dict.get('customer_profile_name')
    new_skills_list = new_skills_list_str.split(',')

    # Optional: Strip any leading/trailing whitespace from each skill
    new_skills_list = [skill.strip() for skill in new_skills_list]
    if not customer_profile_name:
        user = frappe.session.user
        if user == 'Guest' or not user:
            frappe.response["message"] = "you are not authorized"
            frappe.response["http_status_code"] = 400
            return
        customer_profile_doc = frappe.get_last_doc(
            "Customer Profile", filters={"user": user})
        if not customer_profile_doc:
            frappe.response["message"] = "Customer Profile does not exist for user, contact support"
            frappe.response["http_status_code"] = 400
            return
        customer_profile_name = customer_profile_doc.name
    existing_skills = frappe.get_list("Customer Profile Skills", fields=["name", "skill_category_name"],
                                      filters={"customer_profile": customer_profile_name})
    existing_skill_names = [
        skill.skill_category_name for skill in existing_skills]

    # Adding new skills that aren't already associated with the customer profile
    for skill_category in new_skills_list:
        if skill_category not in existing_skill_names:
            new_skill_doc = frappe.get_doc({
                "doctype": "Customer Profile Skills",
                "skill_category_name": skill_category,
                "customer_profile": customer_profile_name
            })
            new_skill_doc.insert()
            existing_skills.append({
                "name": new_skill_doc.name,
                "skill_category_name": skill_category
            })

    # Removing skills that aren't in the new skills list and updating existing_skills list accordingly
    for skill in existing_skills[:]:
        if skill.get("skill_category_name") not in new_skills_list:
            frappe.delete_doc("Customer Profile Skills", skill.name)
            existing_skills.remove(skill)

    # Setting the frappe response message with the updated skills list
    frappe.response["message"] = existing_skills


@frappe.whitelist()
def update_skills():
    # Name of the skill you want to handle
    skill = frappe.form_dict.get('skill')

    # Name of the customer_profile_skill
    customer_profile_skill = frappe.form_dict.get('customer_profile_skill')

    # Construct the unique name based on the naming convention
    skill_name = f"Customer Profile Skills-{customer_profile_skill}-skills-{skill}"

    if frappe.request.method == 'POST':
        # Check if the skill is already associated with the given parent
        if frappe.db.exists("Child Skill", skill_name):
            frappe.response["message"] = "Skill already exists for this parent."
            frappe.response["http_status_code"] = 400
            return

        # Create a new skill
        try:
            added_skill = frappe.get_doc({
                "doctype": "Child Skill",
                "name": skill_name,
                "skill": skill,
                "parent": customer_profile_skill,
                "parenttype": "Customer Profile Skills",
                "parentfield": "skills"
            }).insert()
            frappe.response["message"] = added_skill
            return
        except Exception as e:
            frappe.response["message"] = str(e)
            frappe.response["http_status_code"] = 400
            return

    elif frappe.request.method == 'DELETE':
        # Try to delete the existing skill
        try:
            if frappe.db.exists("Child Skill", skill_name):
                frappe.delete_doc("Child Skill", skill_name)
                frappe.response["message"] = "Skill deleted successfully"
            else:
                frappe.response["message"] = "Skill not found"
                frappe.response["http_status_code"] = 404
            return
        except Exception as e:
            frappe.response["message"] = str(e)
            frappe.response["http_status_code"] = 500
            return
