from django.contrib import admin
from .models import Payment, Order, OrderedFood

# Register your models here.

class OrderedFoodInLine(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    #without the read only fields the items on the admin panel would be editable
    extra = 0 # without this there would be extra fields on the admin panel

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'payment_method', 'status','order_placed_to', 'is_ordered'] #order_placed_to is coming from the Order model
    inlines = [OrderedFoodInLine]
   
  

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
