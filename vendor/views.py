from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from accounts.models import User, UserProfile
from accounts.forms import UserProfileForm 
from .models import vendor, openingHour #here
from django.contrib import messages
from .forms import vendorform, openingHourForm
from accounts.forms import userform
#from django.utils import send_verification_email
from loginout.utils import send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from loginout.views import check_role_vendor
from Menu.models import Category
from Menu.models import fooditem
from Menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from orders.models import Order, OrderedFood

 



# Create your views here.

def get_vendor(request):
    Vendor = vendor.objects.get(user = request.user)
    return Vendor


def registervendor1(request):
    if request.user.is_authenticated: # if the user is logged in they should not ve able to create accont
        messages.warning(request, "you are already logged in")
        return redirect('myaccount')
    
    elif request.method =='POST':
        form = userform(request.POST)
        v_form = vendorform(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #confirm_password = form.cleaned_data['confirm_password']
            user = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                username=username, 
                email=email, 
                password=password, 
                #confirm_password=confirm_password
                )
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
                       
            vendor.vendor_slug = slugify(vendor_name) + '-'+str(user.id) #if a user tries to register a vendor name that already exist then concatenating the user id would make it unique
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #send email verification
            send_verification_email(request, user) #calling from the util class

            messages.success(request, "Your account has been registered succesfully, please wait for approval")
            return redirect(registervendor1)

        else:
            print("invalid form")
            print(form.errors, v_form.errors)

    else:
        form = userform()
        v_form = vendorform()

    context = {

        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registervendor.html', context)


@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def vprofile(request):

    Profile = get_object_or_404(UserProfile, user=request.user) #filtering out the content
    Vendor = get_object_or_404(vendor, user=request.user)# filtering out the content 

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=Profile) #request.files becouse we would e posting photos
        vendor_form = vendorform(request.POST, request.FILES, instance=Vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Records has been updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:

        profile_form = UserProfileForm(instance=Profile) #by passing this instance the form would load the existing data of that form
        vendor_form = vendorform(instance=Vendor) #passing this instance the form would load the existing data of that form

    context = {

        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'Profile': Profile,
        'Vendor': Vendor,


    }

    return render(request, 'vendor/vprofile.html', context)#every other template was calling from the account folder but this one would be calling from vendor folder



@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def MenuBuilder(request):
    Vendor = get_vendor(request)
    categories = Category.objects.filter(Vendor = Vendor).order_by('created_at')# the Vendor in the bracket calls up the Vendor on the first line

    context = {

        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def fooditems_by_category(request, pk=None):
    
    Vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)

    fooditems = fooditem.objects.filter(vendor=Vendor, category=category)
    print(fooditems)

    context = {

        'fooditems': fooditems,
        'category': category


    }


    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def add_category(request):
    if request.method == 'POST':#
        form = CategoryForm(request.POST)#
        if form.is_valid():#
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.Vendor = get_vendor(request)#assigning the logged in user to the Vendor field. Vendor is coming from the Menu Category model
            category.slug = slugify(category_name)# the category_name would be captured from the user inoput on line 160. So it would slugify the catefy_name and pass it to the slug field

            form.save()
            messages.success(request, 'Category added succesfully')
            return redirect('MenuBuilder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {

        'form': form
    }

    return render(request, 'vendor/add_category.html', context)


@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':#
        form = CategoryForm(request.POST, instance=category)# getting the instance of the category
        if form.is_valid():#
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.Vendor = get_vendor(request)#assigning the logged in user to the Vendor field. Vendor is coming from the Menu Category model
            category.slug = slugify(category_name)# the category_name would be captured from the user inoput on line 160. So it would slugify the catefy_name and pass it to the slug field

            form.save()
            messages.success(request, 'Category Updated succesfully')
            return redirect('MenuBuilder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)#Instance = category passes the data of the existing category into the form
    context = {

        'form': form,
        'category': category
    }
    
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'category has been deleted successfully')
    return redirect('MenuBuilder')

@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def add_food(request):
    if request.method == 'POST':#
        form = FoodItemForm(request.POST, request.FILES)# We added request.files before their is an image field
        if form.is_valid():#
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)#assigning the logged in user to the Vendor field. Vendor is coming from the Menu Category model
            food.slug = slugify(foodtitle)# the category_name would be captured from the user inoput on line 160. So it would slugify the catefy_name and pass it to the slug field

            form.save()
            messages.success(request, 'Food item added succesfully')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(Vendor = get_vendor(request))#without thid code the vendor drop down would load all the categori\y list irrespective of the vendor

    context = {

        'form': form,
    }

    return render(request, 'vendor/add_food.html', context)



@login_required(login_url = 'login') 
@user_passes_test(check_role_vendor) 
def edit_food(request, pk=None):
    food = get_object_or_404(fooditem, pk=pk)

    if request.method == 'POST':#
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():#
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request) 
            food.slug = slugify(foodtitle) 
            form.save()
            messages.success(request, 'Food Item Updated succesfully')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)# to make the edit form contain the previously saved data
        form.fields['category'].queryset = Category.objects.filter(Vendor = get_vendor(request))#without thid code the vendor drop down would load all the categori\y list irrespective of the vendor

    context = {

        'form': form,
        'food': food
    }
    
    return render(request, 'vendor/edit_food.html', context)



@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def delete_food(request, pk=None):
    food = get_object_or_404(fooditem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted successfully')
    return redirect('fooditems_by_category', food.category.id)

def opening_hours(request):
    opening_hours = (openingHour.objects.filter(Vendor=get_vendor(request)))

    form = openingHourForm()

    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    
    return render(request, 'vendor/opening_hours.html', context )

from django.http import JsonResponse, HttpResponseBadRequest

from django.http import JsonResponse, HttpResponse
from django.db.utils import IntegrityError

def add_opening_hours(request):
    # Handle data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                hour = openingHour.objects.create(Vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = openingHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'} #If u check the model you would see where get_day_display is coming from 
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                    
                
                return JsonResponse(response)

            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+'already exist for this day'}
                return JsonResponse(response)

        else:
            # Return a 400 Bad Request response for non-AJAX or non-POST requests
            return HttpResponse('Invalid request', status=400)

    else:
        # Return a 401 Unauthorized response for unauthenticated users
        return HttpResponse('Authentication required', status=401)
    
@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(openingHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id':pk})
        

@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request)) #
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'tax_data': order.get_total_by_vendor()['tax_dict'],
            'grand_total': order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')
    return render(request, 'vendor/order_detail.html', context)
        



@login_required(login_url = 'login') #These are decorators
@user_passes_test(check_role_vendor) #These are decorators
def my_orders(request):

    thevendor = vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[thevendor.id], is_ordered=True).order_by('-created_at') 
    
    context = {

        'orders': orders,
    }
    return render(request, 'vendor/my_orders.html', context)
