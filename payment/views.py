from django.shortcuts import render
from .models import ShippingAdress,Order,OrderItem
from cart.cart import Cart
from django.http import JsonResponse
# Create your views here.

def checkout(request):

    # Users with accounts -- Pre-fill the form

    if request.user.is_authenticated:

        try:
            #Authenticated users with shipping information

            shipping_address = ShippingAdress.objects.get(user=request.user.id)

            context = {'shipping':shipping_address}

            return render(request, 'payment/checkout.html', context=context)

        except:

            # Authenticated users with no shipping info
            return render(request, 'payment/checkout.html')

    else:
        #Guest users
        return render(request, 'payment/checkout.html')


def complete_order(request):

    if request.POST.get('action') == 'post':    #Ajax'da 'post' şeklinde yazıyor

        name = request.POST.get('name')  #parantiz içi ajax'dan
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # All-in-one shipping adress
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode)



        # Shopping cart info
        cart = Cart(request)

        # Total Price
        total_cost = cart.get_total()

        '''
            Order variations

            1-) Create order -> Account users with/without shipping info
            
            
        '''
        # 1-) Create order -> Account users with/without shipping info
        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,amount_paid=total_cost, user=request.user)

            order_id = order.pk  #primary key of order

            for item in cart:
                OrderItem.objects.create(order_id=order,product=item['product'], quantity=item['qty'], price=['price'],user=request.user)


        # 2-) Create order -> Guest users without an account
        else:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,amount_paid=total_cost)

            order_id = order.pk  #primary key of order

            for item in cart:
                OrderItem.objects.create(order_id=order,product=item['product'], quantity=item['qty'], price=['price'])
            
        order_success = True

        response = JsonResponse({"success":order_success})

        return response  #birşeyler döndürmemiz lazım


def payment_success(request):

    # Clear shopping cart
    for key in list(request.session.keys()):

        if key == "session_key":

            del request.session[key]


    return render(request, 'payment/payment-success.html')




def payment_failed(request):

    return render(request, 'payment/payment-failed.html')










