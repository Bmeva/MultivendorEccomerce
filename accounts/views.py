from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from .forms import userform
from .models import User
from django.contrib import messages
#from django.utils import send_verification_email
from loginout.utils import send_verification_email





# Create your views here.
def registeruser(request):
    if request.user.is_authenticated: # if the user is logged in they should not ve able to create accont
        messages.warning(request, "you are already logged in")
        return redirect('Dashboard')
    elif request.method == 'POST':
        form = userform(request.POST) # this calls up the form we created in the Forms.py
        if form.is_valid():
            password = form.cleaned_data['password'] #this would get the password and hash it on line 21
            user = form.save(commit=False)
            user.set_password(password) # this would hash the password
            user.role = User.CUSTOMER
            user.save()

            #send verification email
            send_verification_email(request, user)

            messages.success(request, "your account has been registered succesfully")
            # primary, warning, secondary, primary, info and light
            return redirect('registeruser')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = userform

    context = {

        'form':form,


    }

    
    return render(request, 'accounts/registeruser.html', context)
    #return HttpResponse("This is the user registration page")



def registeruser2(request): #second way to register users
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           username = form.cleaned_data['username']
           email = form.cleaned_data['email']
           phone_number = form.cleaned_data['phone_number']
           password = form.cleaned_data['password']
           user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
           user.role = User.CUSTOMER
           user.save()
           return redirect('registeruser')
    else:
        form = userform

    context = {

        'form':form,


    }

    
    return render(request, 'accounts/registeruser.html', context)
    #return HttpResponse("This is the user registration page")

def registeruser(request):
    if request.user.is_authenticated: # if the user is logged in they should not ve able to create accont
        messages.warning(request, "you are already logged in")
        return redirect('Dashboard')
    elif request.method == 'POST':
        form = userform(request.POST) # this calls up the form we created in the Forms.py
        if form.is_valid():
            password = form.cleaned_data['password'] #this would get the password and hash it on line 21
            user = form.save(commit=False)
            user.set_password(password) # this would hash the password
            user.role = User.CUSTOMER
            user.save()

            #send verification email
            send_verification_email(request, user)

            messages.success(request, "your account has been registered succesfully")
            # primary, warning, secondary, primary, info and light
            return redirect('registeruser')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = userform

    context = {

        'form':form,


    }

    
    return render(request, 'accounts/registeruser.html', context)
    #return HttpResponse("This is the user registration page")



