from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import vendor

# STARTING HERE
from django.http import JsonResponse
from django.views import View
from vendor.models import vendor

def home(request):#Loading page
    Vendor = vendor.objects.filter(is_approved=True, user__is_active=True)[:8] #fetches all the approved vendors
    #user and is_approved is coming from the vendor model and in the vendor model user is calling User model
    #which also have the is_active field. that is why we used double for user__is_active.
    #the 8 above would filter the first 8 vendorrs
   
    all_vendors = vendor.objects.all()
    #print(Vendor)
    #print("Vendor names:", [ven1.vendor_name for ven1 in Vendor1])
    context = {
        'all_vendors': all_vendors,
        'Vendor': Vendor
    }
    return render(request, 'home.html', context)





