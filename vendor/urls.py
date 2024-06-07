from django.urls import path
from . import views

from loginout import views as loginoutviews #this would allow me use the views on loginout

urlpatterns = [

    path('', loginoutviews.vendordashboard, name = 'vendor'), #http://127.0.0.1:8000/vendor/ this would open it

    path('registervendor1/', views.registervendor1, name='registervendor1'),

    path('profile/', views.vprofile, name='vprofile'),

    path('MenuBuilder/', views.MenuBuilder, name='MenuBuilder'),

    path('fooditems_by_category/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    #Category Crud
    path('menu-builder/category/add', views.add_category, name='add_category'),

    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),

    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    #FoodItem CRUD

    path('menu-builder/food/add', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    #Opening Hour Crud
    path('opening-hours/', views.opening_hours, name = 'opening_hours'),
    
    #add opening hours
    path('opening-hours/add/', views.add_opening_hours, name = 'add_opening_hours'),
    
    #remoove closing hours
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),
  
    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),

    path('vendor_my_orders/', views.my_orders, name = 'vendor_my_orders')



    

   


       
]