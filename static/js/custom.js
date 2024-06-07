function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_primaryAddress'),
        {
            types: ['geocode'],
            // Use 'GB' for the United Kingdom 
            componentRestrictions: { 'country': ['GB'] },
        }
    );

    // Function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_primaryAddress').placeholder = "Start typing...";
    } else {
        console.log('Place name =>', place.name);
        // Get the address components and assign them to the fields
    }
}

$(document).ready(function () {
    // add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'login_required') {
                    swal(response.message, "Food Vendor App.", "info").then(function () {
                        window.location = '/loginout';
                        //i used sweetalert to display a message box. from .then is to redirect the user 
                        //to the login page

                    });
                } else if (response.status == 'Failed') {
                    // Handle the 'Failed' status, for example, show an error message
                    swal("Oops!", "Something went wrong.", "error");

                } else if (response.cart_counter && response.cart_counter['cart_count'] !== undefined) {
                    console.log(response.cart_counter['cart_count']);
                    //cart_counter is coming from the views.py file in marketplace app under the 
                    //add_to_cart function. cart_count is coming from the context processor which was created on 
                    //marketplace app
                    //alert(response)
                    $('#cart_counter_navbar').html(response.cart_counter['cart_count']);
                    //cart_counter_navbar is the id of the cart item so this code would update the cart item
                    //and increase the quantity each time the plus icon is clicked in the vendor_detail
                    //while cart_count is the context pprocessor that does the count
                    $('#qtyyy-' + food_id).html(response.qty);
                    //qty is coming from the veiws.py
                    //subtotal, tax and grandtotal
                    applyCartAmount( //this is a function written below
                        response.cart_amount['SUBTOTAL'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['TAX'], 
                        response.cart_amount['GRANDTOTAL'],
                    )

                } else {
                    console.error('Invalid response format: cart_counter not found.');
                }
            }

        });
    });



    //place the cart item quantity on load. This was used to display the item quantity on the vendor_detail html
    $('.item_qty').each(function () {

        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#' + the_id).html(qty) //this line is appending the id and quantity

    })

    // Decrease cart
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');


        $.ajax({
            type: 'GET',
            url: url,

            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {

                    alert(response.message);
                    window.location.href = '/loginout';
                    //swal(response.message, "Food Vendor App.", "info").then(function(){
                    // window.location = '/loginout';


                    //});
                } else if (response.status == 'Failed') {

                    swal(response.message, " Food Vendor App", "error");



                } else {

                    $('#cart_counter_navbar').html(response.cart_counter['cart_count']);

                    $('#qtyyy-' + food_id).html(response.qty);

                    applyCartAmount(
                        response.cart_amount['SUBTOTAL'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['TAX'],
                        response.cart_amount['GRANDTOTAL'],
                    )
                    swal('You have reduced the cart item', "Food Vendor App", "success");
                    if (window.location.pathname === '/marketplace/cart/') {
                        //marketplace and the cart page uses almost same functions in the views page
                        //so we call this two conditions below only when we are in the cart page
                        removecartItem(response.qty, cart_id);
                        checckEmptyCart();


                    }

                }



            }



        })


    })

    // delete cart item to delete an entire cart even cart quantity of that item is 5 it deletes everything
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();


        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        $.ajax({
            type: 'GET',
            url: url,

            success: function (response) {
                console.log(response)

                if (response.status == 'Failed') {

                    swal(response.message, " Food Vendor App", "error");



                } else {

                    $('#cart_counter_navbar').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, "success")
                    applyCartAmount(
                        response.cart_amount['SUBTOTAL'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['TAX'], //this
                        response.cart_amount['GRANDTOTAL'],
                    )
                    removecartItem(0, cart_id);
                    checckEmptyCart()

                    // for this funtion i did not check if (response.status == 'login_required') this
                    //beouse i have used the @login decorator on the views function 

                }



            }



        })


    })
    //delete the cart element if the quantity is zero. 
    //This should happen when delete cart has been clicked and all items removed.
    //this function was called up in the delete cart function 
    function removecartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            //remove the cart item element
            document.getElementById('cart-item-' + cart_id).remove()


        }



    }

    //this function checks if the check if the cart item on the navbar is empty and 
    // shows the empty cart label . This function was called up in the delete cart function
    function checckEmptyCart() {
        var cart_counter = document.getElementById('cart_counter_navbar').innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    //apply cart amount
    function applyCartAmount(SUBTOTAL, tax_dict, GRANDTOTAL) {
        if (window.location.pathname == '/marketplace/cart/') {
            $('#subtotal').html(SUBTOTAL);
            $('#TAX').html(TAX); //here
            $('#total').html(GRANDTOTAL);
            

            for(key1 in tax_dict){
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key1][key2])
                }

            }

        }

    }
    $(document).ready(function () {
        // Event listener for dropdown item click
        $('.dropdown-item').on('click', function () {
            // Get the selected vendor name
            var selectedVendor = $(this).data('vendor-name');

            // Update the input text with the selected vendor name
            $('#vendor-search-input').val(selectedVendor);
        });
    });

    //add opening hour
   

    $(document).ready(function () {
        $('.add_hour').on('click', function(e){ //ajax function to add opneing hours in the opening_hours.html it prevents the page from refreshing when adding opening hours
            e.preventDefault();
            var day = document.getElementById('id_day').value //if you inspect the form you would see the id. django explicitely set the id name when we created the form but if you want to set the id name by your self then check the form code below
            var from_hour = document.getElementById('id_from_hour').value
            var to_hour = document.getElementById('id_to_hour').value
            var is_closed = document.getElementById('id_is_closed').checked
            var csrf_token = $('input[name=csrfmiddlewaretoken]').val() // if you inspect the form you would find the name of the csfr token
            var url = document.getElementById('add_hour_url').value
            console.log(day, from_hour, to_hour, is_closed, csrf_token)

         
            if (is_closed) {
                is_closed = 'True'
                condition = "day != ''"
            } else {
                is_closed = 'False'
                condition = "day != '' && from_hour != '' && to_hour !=''"
            }
            if (eval(condition)){
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        'day': day,
                        'from_hour': from_hour,
                        'to_hour': to_hour,
                        'is_closed': is_closed,
                        'csrfmiddlewaretoken': csrf_token,
                    },
                    success: function (response) {
                        if (response.status == 'success') {
                            if (response.is_closed == 'Closed') {

                                html = '<tr id="hour-'+response.id +'"><td><b>'+ response.day +'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/' + response.id + '/">Remove</a></td></tr>';

                            } else {
                                html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                                html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';

                            }

                            $(".opening_hours").append(html)
                            document.getElementById("opening_hours").reset();
                        } else {

                            swal(response.message, '', "error")
                        }

                    }
                })
            } else {
                swal('Please fill all fields', '', 'info')
            }

        })


        //remove opening hour. I can also create a new document ready function for it



    });
    $(document).on('click', '.remove_hour', function(e){
       // window.location.reload();
       e.preventDefault();
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'success') {
                    document.getElementById('hour-' + response.id).remove()
                }
            }
        })

    })
    

});



function payMethodConfirm(){

    //this resets the span on the html after you have selected a payment method
    $('input[name=payment_method]').on('change', function () {
        $('#payment_method_error').html("");
    });

    //this checks if payment method is selected
    var payMethod = $("input[name='payment_method']:checked").val();
    if(!payMethod){
        $('#payment_method_error').html("Select Payment method to continue");
        return false;
        
    }else{
        var conf = confirm('You have selected' + ' '+ payMethod + ' '+ 'as your prefered payment method. \n click "OK" to continue');
        if(conf == true){
            return true;
        }else{
            return false;
        }
    }
    
  
}









/*
class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
        widgets = {
            'day': forms.Select(attrs={'id': 'day'}),
            'from_hour': forms.Select(attrs={'id': 'from_hour'}),
            'to_hour': forms.Select(attrs={'id': 'to_hour'}),
            'is_closed': forms.CheckboxInput(attrs={'id': 'is_closed'}),
        }
    */