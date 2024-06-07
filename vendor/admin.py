from django.contrib import admin
#from .models import vendor this should also work
from vendor.models import vendor, openingHour


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')#when you click it should open the details
    list_editable = ('is_approved',) # if you dont add this then you would need to open the details of
    #the vendor before you can set their approval to true or false. 


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('Vendor','day', 'from_hour','to_hour')
    
# Register your models here.
admin.site.register(vendor, VendorAdmin)
admin.site.register(openingHour, OpeningHourAdmin)