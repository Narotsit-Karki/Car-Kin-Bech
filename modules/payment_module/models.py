from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model
from resale_store_module.models import ResaleCar
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import mail

User = get_user_model()
# Create your models here.
class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        UNPAID = 'UNPAID',_('Unpaid')
        PAID = 'PAID',_('Paid')
        SHIPPED = 'SHIPPED',_('Shipped')
        DELIVERED = 'DELIVERED',_('Delivered')
        CANCELLED = 'CANCELLED',_('Cancelled')

    ISO_CURRENCY_NEPAL = 'npr'
    ISO_CURRENCY_INDIA = 'inr'
    ISO_CURRENCy_DOLLAR = 'usd'

    ISO_CURRENCY = (
        (ISO_CURRENCY_NEPAL,'NPR'),
        (ISO_CURRENCY_INDIA,'INR'),
        (ISO_CURRENCy_DOLLAR,'USD')
    )

    user = models.ForeignKey(to=User,on_delete=models.RESTRICT)
    car = models.ForeignKey(to = ResaleCar,on_delete = models.DO_NOTHING)
    status = models.CharField(choices=OrderStatus.choices,max_length=20,default=OrderStatus.PAID)
    unit = models.CharField(choices = ISO_CURRENCY,max_length=3,default=ISO_CURRENCY_NEPAL)
    amount = models.FloatField()

class Transaction(BaseModel):
    class TransactionType(models.IntegerChoices):
        MOBILE_WALLET = 1,_('Mobile Wallet')
        ONLINE_BANKING = 2,_('Online Banking')
        CREDIT_CARD = 3,_('Credit Card')

    order = models.ForeignKey(to = Order,on_delete=models.RESTRICT)
    amount = models.FloatField()
    note = models.TextField()
    # Transaction_type = models.CharField(choices=)

class Shipping(BaseModel):
    pass

# send customer success email after successfull order creation
@receiver(post_save,sender=Order)
def send_order_success_email(sender:Order,instance:Order,created:bool,**kwargs):
    if created:
        # first time when order is created
        pass
    else:
        if instance.status == Order.OrderStatus.SHIPPED:
            # email when the car is shipped
            pass
        elif instance.status == Order.OrderStatus.DELIVERED:
            # email when the car is delivered
            pass
        elif instance.status == Order.OrderStatus.CANCELLED:
            # email when the car order is cancelled
            pass





