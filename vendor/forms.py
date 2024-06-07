from django import forms
from .models import vendor, openingHour
from accounts.validators import allow_only_images_validator

class vendorform(forms.ModelForm): 
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators= [allow_only_images_validator]) #on the vprofile.htm we called the vendor license to display so this code would give the button a style css
    class Meta:
        model = vendor
        fields = ['vendor_name', 'vendor_license', 'office_phone'] 

# for the vendor registration we need two extra fields which are vendor name and
#  vvendor license thats why we made this form but on the views we called up the userform we used for 
#customer registration

class openingHourForm(forms.ModelForm):
    class Meta:
        model = openingHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']


        
        



