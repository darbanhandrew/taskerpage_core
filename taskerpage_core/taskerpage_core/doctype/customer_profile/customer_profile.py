# Copyright (c) 2023, Mohammad Darban Baran and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import json

class CustomerProfile(Document):
    @property
    def map_view(self):
        geojson = {
            "type": "Feature", 
            "properties": {}, 
            "geometry": {
                "type": "Point", 
                "coordinates": [self.latitude, self.longitude]
            }
        } if self.longitude is not None and self.longitude is not None else {
            "type": "FeatureCollection", 
            "features": []
        }
        return json.dumps(geojson)
    
    def on_update(self):
        self.set_personal_details_completed()

    def set_personal_details_completed(self):
        required_fields_for_individual = ['first_name', 'last_name', 'phone_number', 'date_of_birth']
        
        # If the account_type is 'company', add 'company_name' to the list of required fields
        if self.account_type == 'company':
            required_fields_for_individual.append('company_name')
        
        # Check if all required fields have values
        self.personal_details_completed = int(all([getattr(self, f) for f in required_fields_for_individual]))
