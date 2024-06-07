from django.urls import path
from . import views



urlpatterns = [

    path('', views.marketplace, name='marketplace'),
    #path('<slug:vendor_slug>', views.vendor_detail, name= 'vendor_detail'), i can also make the path like this
    path('vendor_detail/<slug:vendor_slug>', views.vendor_detail, name= 'vendor_detail'),

    #add to cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),

     #Decrese cart
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),

    #The cart page
    path('cart/', views.cart, name='cart'),

    #Dleete cartitem
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),


    #Add tax
    path('add-tax/tax/addtax', views.add_tax, name='add_tax'),
    #To access this link directly use http://127.0.0.1:8000/marketplace/add-tax/tax/addtax

   


]