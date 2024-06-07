from django.contrib import admin

# Register your models here.


from .models import Category, fooditem


class CategoryAdmin(admin.ModelAdmin):# this code would make the eslug field get automatically createed as you type the category name
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'Vendor', 'updated_at')
    search_fields = ('category_name', 'Vendor__vendor_name')
    #vendor_name is the field in the vendor model. Vendor is the field we want to search which is in the 
    #menu model howver it is a foreign key that is why we put __ and the vendor_name
    #You can search by the category name of the vendor name from the admin dashboard

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)
    


admin.site.register(Category, CategoryAdmin)
admin.site.register(fooditem, FoodItemAdmin)