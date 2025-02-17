from django import forms
from .models import Category, fooditem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator]) #w-100 means width 100 percent
    class Meta:
        model = fooditem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']
