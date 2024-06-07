from .models import Cart
from Menu.models import fooditem
from decimal import Decimal
from .models import Tax

#this context processing was made becouse the cart is on the navbar and we want to access it
#all over the website. we have to reguster the ocntext processor in settings.py for it to work.
#this function was called on the navbar.html as cart_count
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count = cart_count)



#Context processor to calculate subtotal and grand total
def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total =0
    tax_dict ={}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            FoodItem = fooditem.objects.get(pk=item.fooditem.id)
            subtotal += (FoodItem.price * item.quantity) # this means subtotal + (fooditem.price * item.quantity)
            #subtotal = subtotal + (FoodItem.price * item.quantity)
        get_tax = Tax.objects.filter(is_active = True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
               
            tax_dict.update({tax_type: {str(tax_percentage) : tax_amount}}) #without the str my cart items did not work again

             
        tax = sum(x for key in tax_dict.values() for x in key.values()) 
        
        grand_total = subtotal + tax
        
    return dict(SUBTOTAL=subtotal, TAX=tax, GRANDTOTAL=grand_total, tax_dict=tax_dict)




""" 
def get_cart_amount2(request):
    subtotal = Decimal('0.0')
    tax = Decimal('0.0')
    grand_total = Decimal('0.0')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            FoodItem = fooditem.objects.get(pk=item.fooditem.id)
            subtotal += Decimal(FoodItem.price * item.quantity) # this means subtotal + (fooditem.price * item.quantity)
            tax = Decimal('0.15') * subtotal
        grand_total = subtotal + tax
          
    return dict(SUBTOTAL=subtotal, TAX=tax, GRANDTOTAL=grand_total)

"""
    
