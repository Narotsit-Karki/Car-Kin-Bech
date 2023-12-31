from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseServerError
from django.http.response import JsonResponse
import stripe
from stripe.error import StripeError
from .models import ResaleCar
import os
from django.contrib.auth.decorators import login_required

# Create your views here.
stripe.api_key = os.environ.get("STRIPE_API_KEY_TEST")
DOMAIN_URL = 'http://localhost:8000'
PAISA  = 100

@login_required
def checkout(request):
    template = "checkout.html"
    return render(request,template_name=template)

@login_required
def create_checkout_session(request,vin):
    if request.method == "POST":
        resale_car = get_object_or_404(ResaleCar,vehicle_identification_number = vin)
        try:  
            product = stripe.Product.create(name = resale_car.fullname,
                                            images = ["https://imgd.aeplcdn.com/1056x594/n/t5acs0b_1641691.jpg?q=80",]
                                        )
            product_price = stripe.Price.create( 
                product = product , unit_amount = int(resale_car.price*1e6), currency = 'npr'
                )

            stripe_checkout_session = stripe.checkout.Session.create(
                # ui_mode = "embedded",
                line_items = [{"price":product_price,"quantity":1}],
                success_url = DOMAIN_URL + "/payment/payment-success",
                cancel_url = DOMAIN_URL + "/payment/payment-cancel",
                mode = 'payment',
                phone_number_collection = {
                    'enabled':True
                },
                shipping_address_collection = {
                    'allowed_countries':['NP']
                },
                shipping_options = [{
                    'shipping_rate_data': {
                        'display_name':'Shipping Cost',
                        'type':'fixed_amount',
                        'fixed_amount':{
                            'currency':'npr',
                            'amount':1500 * PAISA
                        },
                        'delivery_estimate':{
                            'maximum': {
                                'unit':'day',
                                'value':7
                            },
                            'minimum':{
                                'unit':'day',
                                'value':5
                            }
                        }
                        
                    }
                },]
            )
              
            return redirect(to=stripe_checkout_session.url)

        except StripeError as err:
            print(err)
            redirect("payment/checkout")
        
        
    else:
        raise HttpResponseNotAllowed(permitted_methods=['POST'])

@login_required    
def payment_success(request):
    template = "payment_success.html"
    return render(request,template_name=template)
@login_required
def payment_cancel(request):
    template = "payment_cancel.html"
    return render(request,template_name=template)
