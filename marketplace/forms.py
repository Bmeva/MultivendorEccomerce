from django import forms
from .models import Tax

class TaxModelForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['tax_type', 'tax_percentage', 'is_active']

        
        



