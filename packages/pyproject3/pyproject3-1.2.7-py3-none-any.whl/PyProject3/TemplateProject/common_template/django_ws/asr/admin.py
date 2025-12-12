from django.contrib import admin
from django_jsonform.widgets import JSONFormWidget
from django_pydantic_field.v2.fields import PydanticSchemaField

from .models import AsrApp, AsrRecord


@admin.register(AsrApp)
class AsrAppAdmin(admin.ModelAdmin):
    search_fields = ["_id"]
    formfield_overrides = {
        PydanticSchemaField: {"widget": JSONFormWidget},
    }

    def get_list_display(self, request):
        return [f.name for f in self.model._meta.fields]


@admin.register(AsrRecord)
class AsrRecordAdmin(admin.ModelAdmin):
    search_fields = ["_id", "app_id", "session_id"]

    def get_list_display(self, request):
        return [f.name for f in self.model._meta.fields]


# @admin.register(HotWords)
# class HotWordAdmin(admin.ModelAdmin):
#     search_fields = ["id", "word", "app__name"]

#     def app_name(self, obj):
#         return obj.app.name

#     def get_list_display(self, request):
#         return [f.name for f in self.model._meta.fields]


# @admin.register(SubstituteWords)
# class TermModificationAdmin(admin.ModelAdmin):
#     search_fields = ["id", "org_term", "des_term", "app__name"]

#     def app_name(self, obj):
#         return obj.app.name

#     def get_list_display(self, request):
#         return [f.name for f in self.model._meta.fields]
