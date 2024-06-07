from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from .utils import detectuser
from .utils import send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from accounts.models import User
from django.contrib.auth.tokens import default_token_generator
from vendor.models import vendor
import os
from orders.models import Order
import datetime

# Create your views here.


# Restrict vendor from accesing customer dashboard
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

#Restrict customer from accesing the vendor dashboard
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied




def login(request):
    if request.user.is_authenticated: #restricts users from accesing login page
        messages.warning(request, "you are already logged in")
        return redirect('myaccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if not email:
            messages.error(request, 'email field cannot be empty')
        elif not password:
            messages.error(request, 'Password field cannot be empty')
        
        else:
            user = auth.authenticate(email=email, password=password) #This checks for the user with the email and password
        #the auth.authenticate comes from django.contrib
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'you are now logged in')
                return redirect('myaccount')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')


    return render(request, 'accounts/login.html')


"""
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myaccount')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not email:
            messages.error(request, 'Email field cannot be empty')
        elif not password:
            messages.error(request, 'Password field cannot be empty')
        else:
            user = User.objects.get(email=email)# I mannually filtered it instead of using the authenticate function
            if user.check_password(password):
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'you are now logged in')
                    return redirect('myaccount')
                    
                   
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('login')

          
                
    return render(request, 'accounts/login.html')
"""



def logout(request):
    auth.logout(request)
    messages.info(request, "you are now logged out")
    return redirect('login')

@login_required(login_url = 'login')
def myaccount(request):
    user = request.user
    redirecturl = detectuser(user)
    return redirect(redirecturl)

@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_customer)
def customerdashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True) 
    recent_orders = orders[:5] #to display the first 5 orders
    
    context = {

         'orders': orders,
         'orders_count': orders.count(),
         'recent_orders': recent_orders
    

    }
   
    return render(request, 'accounts/customerdashboard.html', context)



@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendordashboard(request): #this code is filering all the order that belongs to the logged in user

    thevendor = vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[thevendor.id], is_ordered=True).order_by('-created_at') 
    
    recent_orders = orders[:5]
    
    #current month revenue

    current_month = datetime.datetime.now().month
    current_months_orders = orders.filter(vendors__in=[thevendor.id], created_at__month=current_month) #these lines are explained in at the bottom
    current_month_revenue = 0
    for i in current_months_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']
   

    #total revenue
    total_revenue = 0
    for i in orders:
        total_revenue +=i.get_total_by_vendor()['grand_total']    #get_total_by_vendor is a function in the order model
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    # when you create a many to many field django creates a third database table which holds the id's
    #in our order model we created vendors = models.ManyToManyField(vendor, blank=True) that is why we are ale to use thevendor.id
    #if you go to pgadmin you would see the additional table called orders_order_vendors but order_order is the app name and the order model table
    #vendors=[vendor.id], is_ordered=True  vendors is coming from the orders_order_vendors table. 
    #right click on it and view data and all rows and you would see the order id and the vendors it belongs to (many to many relationships)
    
   
    return render(request, 'accounts/vendordashboard.html', context)


# Login required and user passes test comes from django.contrib.auth.decorators import login_required, user_passes_test

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists(): #checking if the inputed email is in the db
            user = User.objects.get(email__exact=email)# getting the exact email address of what the user entered. exact is case sensitive but iexact is not

            #send reset password email
            send_password_reset_email(request, user)#calling this from util.py
            messages.success(request, 'Password reset link have been sent to yout email address')
            return redirect('login')
        
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
  

    return render(request, 'accounts/forgot_password.html')




def reset_password_validate(request, uidb64, token): #This method was called up in the reset_password_email.html
    #validate the user by decoding the token and user primary key
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, "This link has expired")
        return redirect('myaccount')
    
     



def reset_password(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not password:
            messages.error(request, 'Password field cannot be emty')
        elif len(password) < 6:
            messages.error(request, "Password must be 6 characters")
        elif not confirm_password:
            messages.error(request, "Confirm password field cannot be empty")
        
        elif password != confirm_password:
            messages.error(request, 'password fields do not match')

                 
        else:
            pk = request.session.get('uid') #the uid was gotten from the reset_password_validate function
            user = User.objects.get(pk = pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset succesful')
            return redirect('login')

    return render(request, 'accounts/reset_password.html')


    


    Notes

"""
In the code created_at__month, the __month is a lookup filter used in Django's queryset API to
filter objects based on the month component of a date field.

Here's how it works:

created_at: This refers to the field in the model that represents the creation timestamp of an object.
__month: This is a lookup filter that extracts the month component from the created_at field and allows 
you to filter objects based on that month.
For example, if you have a created_at field in your model that stores timestamps, you can use
 created_at__month=2 to filter objects created in February (where 2 represents the month of February). 
 Similarly, you can use other integer values to filter objects based on different months.

 
 In the code vendors__in=[thevendor.id], the vendors field is a ManyToManyField in the Order 
 model, and it's likely a reference to vendors associated with an order. you would see it 
 as order_order_vendor table in the database

"""