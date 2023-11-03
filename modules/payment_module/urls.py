from django.urls import path
from .views import *


urlpatterns = [
    path('create-checkout-session/<vin>', create_checkout_session,name='stripe_checkout_session_create'),
    path('checkout',checkout,name="checkout"),
    path('payment-sucess',payment_success,name="payment_success"),
    path("payment-cance",payment_cancel,name="payment_cancel")
]