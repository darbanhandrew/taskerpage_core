# Copyright (c) 2023, Mohammad Darban Baran and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import json
class CustomerTask(Document):
	@property
	def map_view(self):
		geojson = {"type": "Feature", "properties": {}, "geometry": {"type": "Point", "coordinates": [self.appointment_location_lat, self.appointment_location_lng]}} if self.appointment_location_lat is not None and self.appointment_location_lng is not None else {"type": "FeatureCollection", "features": []}
		return json.dumps(geojson)
