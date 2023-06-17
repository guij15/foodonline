from django.contrib import admin
from vendor.models import Vendor
# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display=['vendor_name','user','is_approved','created_at','modified_at']
    list_display_links=['vendor_name','user']
    list_filter=['is_approved']
    search_fields=['vendor_name']
    list_editable=['is_approved']

admin.site.register(Vendor,VendorAdmin)