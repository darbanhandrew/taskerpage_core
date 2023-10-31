# Copyright (c) 2023, Mohammad Darban Baran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FollowRequest(Document):

    def on_update(self):
        # Check if the FollowRequest status is 'Accepted'
        if self.status == 'Accepted':
            # Add requestor to the following list of the requested user
            self._add_to_list(
                user_profile=self.requested_user,
                list_type='followers',
                customer_profile_to_add=self.requestor,
                user_to_add=self.requestor_user
            )

            # Add requested to the followers list of the requestor user
            self._add_to_list(
                user_profile=self.requestor_user,
                list_type='following',
                customer_profile_to_add=self.requested_user,
                user_to_add=self.requested_user
            )

    def _add_to_list(self, user_profile, list_type, customer_profile_to_add, user_to_add):
        """Add a profile to a specified list (followers or following) of a User."""
        # Check if the user is already in the list to prevent duplicates
        existing_entry = frappe.get_all("Followers", filters={
            "parent": user_profile,
            "parenttype": "User",
            "follower_user": user_to_add
        })

        if existing_entry:
            # If the user is already in the list, just return
            return

        # Insert the new follower/following into the child table
        frappe.get_doc({
            "doctype": "Followers",
            "follower": customer_profile_to_add,
            "follower_user": user_to_add,
            "parent": user_profile,
            "parenttype": "User",
            "parentfield": list_type
        }).insert(ignore_permissions=True)
