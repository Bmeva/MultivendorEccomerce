from django.shortcuts import render, redirect
from marketplace.models import Cart

from django.contrib import messages
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order
from django.http import JsonResponse

from .utils import generate_order_number, order_total_by_vendor

from django import forms
from django.http import HttpResponse
from .models import Payment
from .models import OrderedFood

from loginout.utils import send_notification
from django.contrib.auth.decorators import login_required
from Menu.models import fooditem
from marketplace.models import Tax
import json
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

@login_required(login_url='login')
def place_order(request):
    #checking if the cart items are zero and sending back the user to the market place if it is 0
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    #Ends here

    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids: #vendor.id is the many to many field we created in the order model. If you check loginout vendordashboard you would see the explanation of the many to many field
            vendors_ids.append(i.fooditem.vendor.id)


    #getting subtotal for each vendor in an order
    get_tax = Tax.objects.filter(is_active = True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        food_item = fooditem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
                
        #food_item = fooditem.objects.get(pk=i.fooditem.id, vendor_id=i.fooditem.vendor.id)

        v_id = food_item.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (food_item.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (food_item.price * i.quantity)
            k[v_id] = subtotal
        

        #calculate the tax_data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}}) #without the str my cart items did not work again
        
        total_data.update({food_item.vendor.id: {str(subtotal): str(tax_dict)}})
        #total_data_json = json.dumps(total_data)
    print("Total data:", total_data)

    
    subtotal = get_cart_amount(request)['SUBTOTAL']
    total_tax = get_cart_amount(request)['TAX']
    grand_total = get_cart_amount(request)['GRANDTOTAL']
    tax_data = get_cart_amount(request)['tax_dict'] #these values in the [] are coming from the fields in the get_cart_amount
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order() #Order is the Order model becouse we want to save the form in the Order model
            #while saving other forms the model is specified in the forms.py
            order.first_name = form.cleaned_data['first_name'] #first_name is coming from the OrderForm and we want to pass it into the first_name field in the model
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user= request.user
            order.total = grand_total
            order.tax_data = JsonResponse(tax_data).content.decode('utf-8')
            
            order.total_data = json.dumps(total_data)
          
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method'] #payment_method is coming from the html page which is the name of the radio button
            if not all([order.first_name, order.last_name, order.phone, order.email, order.address, order.country, order.state, order.city, order.pin_code]):
                
                messages.error(request, 'all fields are required')
                return redirect('checkout') # this checkout url is configured in the mealsonline app
             
      
            else:
            
                order.save() # we have to save it first so that the pk or id would be craeted before passing it to the ordser number
                order.order_number = generate_order_number(order.id)
                order.vendors.add(*vendors_ids) #we added * so it would add it to the many to many field we created. check vendordashboar in loginout for explanation
                order.save()
                context = {
                    'order': order,
                    'cart_items': cart_items,
                }
                return render(request, 'orders/place_order.html', context)


        else:
            messages.error(request, 'Form submission error. Please check the data.')
            print(form.errors)
    return render(request, 'orders/place_order.html')


#this views is connected to the ajax call on the place_order page on line 184 where i have  var url = "{% url 'payments' %}"
@login_required(login_url='login')
def payments(request):
    
    #check if request is ajax or not
    if request.headers.get('x-requested-with') =='XMLHttpRequest' and request.method == 'POST':
        #Store the payment details in the payment model
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST['status']
        print(order_number, transaction_id, payment_method, status)

        
        order = Order.objects.get(user=request.user, order_number=order_number)

        #in this Payment model we have transaction_id, payment_method, amount and status so we are getting the details and sending to the order model
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()
        #Update the order model when payment is saved
        order.payment = payment
        order.is_ordered = True
        order.save()
        #return HttpResponse('Saved')
     
    #Move the cart items to the ordered food model
        cart_items = Cart.objects.filter(user = request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            ordered_food.save()
      
        #send order confirmation email to the customer
               
        vendor_names_set = set(item.fooditem.vendor.user.first_name for item in cart_items)
        
        mail_subject = "Thank you for your order"
        mail_template = 'orders/order_confirmation_email.html'
        ordered_food = OrderedFood.objects.filter(order=order)
        customer_subtotal = 0
        for item in ordered_food:
            customer_subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        domain = get_current_site(request)
        vendor_names_set = set(item.fooditem.vendor.user.first_name for item in cart_items)
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
            'ordered_food': ordered_food,
            'vendor_names': list(vendor_names_set), # i put it in a list so it wont list a vendor more than once
            'domain': domain,
            'customer_subtotal': customer_subtotal,
            'tax_data': tax_data,
        }
        send_notification(mail_subject, mail_template, context)

          
        #SEND ORDER RECEIVED email TO THE VENDOR
        mail_subject = "You have received a new order"
        mail_template = 'orders/new_order_received_email.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)

            ordered_food_to_vendor = OrderedFood.objects.filter(order=order, fooditem__vendor= i.fooditem.vendor)
            #the above would give you vendor specific ordered food
            
               
        for vendor in cart_items.values_list('fooditem__vendor__vendor_name', flat=True).distinct():
            vendor_cart_items = cart_items.filter(fooditem__vendor__vendor_name=vendor)

            context = {
                'order': order,
                'to_email': i.fooditem.vendor.user.email,
                'vendor_name': vendor,
                'ordered_food_to_vendor': ordered_food_to_vendor,
                'vendor_subtotal': order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'], #order_total_by_vendor is coming from util.py. and the function also have a subtotal which i accessed
                'tax_data': order_total_by_vendor(order, i.fooditem.vendor.id)['tax_dict'], #order_total_by_vendor is coming from util.py. and the function also have a tax_dict which i accessed
                'vendor_grand_total': order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total'] #order_total_by_vendor is coming from util.py. and the function also have a grand_total which i accessed
                       
            } 
            send_notification(mail_subject, mail_template, context)
        

        #Clear the cart if the payment is success
        cart_items.delete()
        

        #treturn back to ajax with success or failure
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)

    return HttpResponse('payments views')

def order_complete(request):
    order_number = request.GET.get('order_no') # It retrieves the order number and transaction ID from the query parameters in the URL using request.GET.get('order_no') and request.GET.get('trans_id').
    #i passed order_number and transaction_id to the URL through the ajax on line 235
    transaction_id = request.GET.get('trans_id')
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        #payment__transaction_id indicates that you are querying a field named transaction_id within the related model payment hence we used the double underscore
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for items in ordered_food:
            subtotal += (items.price * items.quantity)
        
        tax_data = json.loads((order.tax_data))

        

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
            
        }
        return render(request, 'orders/order_complete.html', context)

    except:
        return redirect('home')
    


