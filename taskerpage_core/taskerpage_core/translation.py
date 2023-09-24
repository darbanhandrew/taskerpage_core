from frappe.model.document import Document
import frappe
class TranslatedDocument(Document):
    @property
    def translations(self):
        #get all document fields which are translatable, and return the translated text
        #the response should be like "{"en":{"field1":"translation"}}"
        #get language from user settings
        lang_code = frappe.local.lang or "en"
        # get all the translatable fields
        meta = frappe.get_meta(self.doctype)
        translatable_fields = meta.get_translatable_fields()
        translated_text = {}
        for field in translatable_fields:
            #get translation for field
            try:
                translated_field_value = frappe.get_last_doc("Translation", filters=[["source_text","=",self.get(field)], ["language","=",lang_code]])
                #check for null safety to return the source text if translation is not found	
                translated_text[field] = translated_field_value and translated_field_value.translated_text or self.get(field)
            except Exception as e:
                translated_text[field] = self.get(field)
        return str(translated_text)

#apps/frappe/frappe/core/doctype/doctype/doctype.py
# def set_base_class_for_controller(self):
#     """If DocType.has_web_view has been changed, updates the controller class and import
#     from `WebsiteGenertor` to `Document` or viceversa"""

#     if not self.has_value_changed("has_web_view"):
#         return

#     despaced_name = self.name.replace(" ", "_")
#     scrubbed_name = frappe.scrub(self.name)
#     scrubbed_module = frappe.scrub(self.module)
#     controller_path = frappe.get_module_path(
#         scrubbed_module, "doctype", scrubbed_name, f"{scrubbed_name}.py"
#     )

#     document_cls_tag = f"class {despaced_name}(Document)"
#     document_import_tag = "from frappe.model.document import Document"
#     website_generator_cls_tag = f"class {despaced_name}(WebsiteGenerator)"
#     website_generator_import_tag = "from frappe.website.website_generator import WebsiteGenerator"
#     doctype_translatable_tag = f"class {despaced_name}(TranslatedDocument)"
#     doctype_translatable_import_tag = "from taskerpage_core.taskerpage_core.taskerpage_core.translation import TranslatedDocument"


#     with open(controller_path) as f:
#         code = f.read()
#     updated_code = code

#     is_website_generator_class = all(
#         [website_generator_cls_tag in code, website_generator_import_tag in code]
#     )

#     if self.has_web_view and not is_website_generator_class:
#         updated_code = updated_code.replace(document_import_tag, website_generator_import_tag).replace(
#             document_cls_tag, website_generator_cls_tag
#         )
#     elif not self.has_web_view and is_website_generator_class:
#         updated_code = updated_code.replace(website_generator_import_tag, document_import_tag).replace(
#             website_generator_cls_tag, document_cls_tag
#         )
#     if self.doctype_translatable:
#         updated_code = updated_code.replace(document_cls_tag, doctype_translatable_tag).replace(
#             document_import_tag, doctype_translatable_import_tag
#         )


#     if updated_code != code:
#         with open(controller_path, "w") as f:
#             f.write(updated_code)