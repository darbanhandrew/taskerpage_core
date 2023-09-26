# Copyright (c) 2023, Mohammad Darban Baran and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import json
class CustomerAddress(Document):
	@property
	def map_view(self):
		geojson = {"type": "Feature", "properties": {}, "geometry": {"type": "Point", "coordinates": [self.latitude, self.longitude]}} if self.latitude is not None and self.longitude is not None else {"type": "FeatureCollection", "features": []}
		return json.dumps(geojson)
