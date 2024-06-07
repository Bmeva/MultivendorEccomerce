from django.urls import path
from loginout import views as loginoutViews
from . import views

urlpatterns = [

    path('', loginoutViews.customerdashboard, name='customer'),
    #the customerdashboard view is in loginout so i want if someone type http://127.0.0.1:8000/customer/ it should still open the page

    path('profile/', views.cprofile, name='cprofile'), #the path would be http://127.0.0.1:8000/customer/profile/

   
    path('Myorders/', views.Myorders, name='Customer_Myorders'),

    path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),



    
]