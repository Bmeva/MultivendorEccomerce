from django.urls import path
from . import views
from . import utils

urlpatterns = [

    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('myaccount/', views.myaccount, name='myaccount'),

    path('vendordashboard/', views.vendordashboard, name='vendordashboard'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),

    path('activate/<uidb64>/<token>/', utils.activate, name='activate'),


    path('forgot_password/', views.forgot_password, name='forgot_password'),
    
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),


    
    
   


     

   
    
]