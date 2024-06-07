from django.urls import path
from . import views

from loginout import views as loginoutviews #this would allow me use the views on loginout app

urlpatterns = [

   
    path('', loginoutviews.myaccount, name = 'myaccount'), #http://127.0.0.1:8000/accounts would open it. on the main project url we configured a path for account 
    #url and this is an empty url which takes it to default when you type accounts

    path('registeruser/', views.registeruser, name='registeruser')
    

   
    
]