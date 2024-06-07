from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from vendor.models import vendor, openingHour
from Menu.models import Category
from django.db.models import Prefetch
from Menu.models import fooditem
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from datetime import date, datetime

from .forms import TaxModelForm
from django.contrib import messages
from django.shortcuts import redirect
from loginout.views import check_role_vendor

from orders.forms import OrderForm
from accounts.models import UserProfile




import pdb

# Create your views here.

@login_required(login_url='login')
def marketplace(request): # this is used if you simply click on market place.
    Vendor = vendor.objects.filter(is_approved=True, user__is_active=True)
    Vendor_counter = Vendor.count()
    context = {

        'Vendor': Vendor,
        'thevencount': Vendor_counter,
    }
    return render(request, 'marketplace/listing.html', context)



def search(request): #this search is used on the home page to search for vendors or food and displays the search in listing.html
    #radius = request.GET['radius']
    address = request.GET['address']
    keyword = request.GET['keyword']
   
    fetch_vendor_food_item = fooditem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
    
    Vendor = vendor.objects.filter(Q(id__in=fetch_vendor_food_item) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))

    Vendor_counter = Vendor.count()
   
    context = {
        
        'Vendor': Vendor,
        'thevencount': Vendor_counter,
    }
    
    return render(request, 'marketplace/listing.html', context)



def vendor_detail(request, vendor_slug):
    Vendor = get_object_or_404(vendor, vendor_slug = vendor_slug)
    categories  = Category.objects.filter(Vendor=Vendor).prefetch_related( #we wanted to get all food items related to the specific categort
        #Howcer we dont have a foregin key in the Category models that links to the fooditem. that is why we used to prefetch methord
        Prefetch(
            'fooditems', #this was set in the fooditem category model field
            queryset = fooditem.objects.filter(is_available=True)
        )
    ) # if i dont filter and use all then it would bring out all categories
    #categories  = Category.objects.all()
    opening_hours = openingHour.objects.filter(Vendor=Vendor).order_by('day', '-from_hour')
    # Check current day's opening hour
    today_date = date.today()
    today = today_date.isoweekday() #gets 1, 2,3 etc according to the number of the week
    current_day_opening_hour = openingHour.objects.filter(Vendor=Vendor, day = today)
    #Checking if restaurant is open and displaying the status close to the vendor name at the top of the page
   
          
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None


    context = {

        'Vendor': Vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_day_opening_hour': current_day_opening_hour,
    
        
    }
    return render(request, 'marketplace/vendor_detail.html', context)


#In this version, the code checks the HTTP_X_REQUESTED_WITH header to determine whether the 
#request is an AJAX request the one below does not check. This request is coming from the 
#javascript add_to_cart function. so when the html is clicked on the vendor_detail plus icon it 
#triggers the javascript
def add_to_cart(request, food_id): 
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        #if request.is_ajax():
            #Check if the fooditem exist
            try:
                FoodItem = fooditem.objects.get(id=food_id)
                #Check if the user has already added the food item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=FoodItem ) #fooditem is a foregin key calling from the Cart model
                    #Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 
                                         'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=FoodItem, quantity=1) #fooditem is a foregin key calling from the Cart model
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 
                                         'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        
    else:
         return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})
    

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        
            try:
                FoodItem = fooditem.objects.get(id=food_id)
               
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=FoodItem ) #fooditem is a foregin key calling from the Cart model
                    if chkCart.quantity > 1:

                    #Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0

                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})


            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})

            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})

        

    else:
         return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})


@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
         if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
             try:
                 #check if the cart item exist
                 cart_item = Cart.objects.get(user=request.user, id=cart_id)
                 if cart_item:
                     cart_item.delete()
                     return JsonResponse ({'status': 'Success', 'message': 'Cart Item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
             except:
                  return JsonResponse ({'status': 'Failed', 'message': 'Cart item does not exist'})
                 
         else:
             return JsonResponse ({'status': 'Failed', 'message': 'Invalid request'})

    

def add_to_cart2(request, food_id):
    if request.user.is_authenticated:
        # Check if the food item exists 
        try:
            food_item = fooditem.objects.get(id=food_id)
            # Check if the user has already added the food item to the cart
            try:
                chkCart = Cart.objects.get(user=request.user, fooditem=food_item)
                # Increase the cart quantity
                chkCart.quantity += 1
                chkCart.save()
                return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity'})
            except Cart.DoesNotExist:
                # If the user hasn't added the food item to the cart, create a new cart entry
                chkCart = Cart.objects.create(user=request.user, fooditem=food_item, quantity=1)
                return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart'})
        except fooditem.DoesNotExist:
            return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please log in to continue'})
    




@user_passes_test(check_role_vendor)
@login_required(login_url = 'login')
def add_tax(request):
#Create a side bar for manupulating tax and other fuctions
    allowed_username = 'evafoodV' #making sure than only this user have access to this page
    if request.user.username != allowed_username:
        messages.error(request, 'Access denied. You are not allowed to access this page.')
        return redirect('logout')
    
    if request.method == 'POST':#
        form = TaxModelForm(request.POST)
        if form.is_valid():#
                     
            form.save()
            messages.success(request, 'Tax has been added succesfully')
            return redirect('add_tax')
        else:
            messages.error(request, 'Form submission error. Please check the data.')
            print(form.errors)

    else:
        form = TaxModelForm()
       
    context = {

        'form': form,
    }

    return render(request, 'marketplace/add_tax.html', context)

@login_required(login_url = 'login')
def checkout(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        messages.error(request, "You dont have any items in your cart")
        return redirect('marketplace')
        
        
    #I am trying to prepopulate the form but it is different from how i populated 
    #the customer profile form in the cutomer app(cprofile).
    #this form is generated from the order app form so we want to prepopulate the form with 
    # the values of the logged in user while we retrive address, country, city, pin code and state from the UserProfile model

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.full_address,
        'country': user_profile.country, #yser_profile is coming from the top where we said user_profile = UserProfile.objects.get 
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
        


    }
    form = OrderForm(initial = default_values)
    context = {
        'form': form,
        'cart_items': cart_items
    }

    
    return render(request, 'marketplace/checkout.html', context)






    






