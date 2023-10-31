from django.db import models
from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class ResaleCarDetail(BaseModel):
      
    class BrandType(models.IntegerChoices):
        pass
    
    class InsuranceType(models.TextChoices):
        FIRST_PARTY = 1,_('1st Party')
        SECOND_PARTY = 2,_('2nd Party')
        THIRD_PARTY = 3,_('3rd Party')
        COMPREHENSIVE = 4,_('Comprehensive')
        ZERO_DEPRECIATION = 5,_('Zero Depriciation')
        Nan = 0,_('Nan')
    
    class EngineType(models.IntegerChoices):
        PETROL = 1,_('Petrol')
        DIESEl = 2,_('Diesel')
        LPG = 3,_('LPG')
        CNG = 4,_('CNG')
        ELECTRIC = 5,_('Electric')
        Nan = 0,_('Nan')
        
    class TransmissionType(models.IntegerChoices):
        MANUAL = 1,_('Manual')
        AUTOMATIC = 2,_('Automatic')
        Nan = 0,_('Nan')
        
    class BodyType(models.IntegerChoices):
        Nan = 0,_('Nan')
    
    class City(models.IntegerChoices):
        Nan = 0,_('Nan')
    
    class BrandType(models.IntegerChoices):
        Nan = 0,_('Nan')

    brand = models.IntegerField()
    model = models.CharField(max_length=150)
    insurance_type = models.IntegerField(choices=InsuranceType.choices,default=InsuranceType.Nan)
    engine_type = models.IntegerField(choices=EngineType.choices,default=EngineType.Nan)
    engine_capacity = models.IntegerField(default=0)
    kms_driven = models.BigIntegerField()
    no_of_seat = models.IntegerField(null = False,blank=False)
    transmission_type = models.IntegerField(choices=TransmissionType.choices,default=TransmissionType.Nan)
    mileage = models.FloatField()
    registered_year = models.IntegerField()
    max_power = models.FloatField()
    body_type = models.CharField(choices=BodyType.choices,default=BodyType.Nan,max_length=20)
    city = models.IntegerField(choices=City.choices,default=City.Nan)

    def __str__(self):
        return f"{self.brand} {self.model} {self.registered_year}"
        

class PreviousOwner(BaseModel):
    fullname = models.CharField(max_length=255,null=False,blank=False,default='Nan')
    contact_phone = models.BigIntegerField(null=False,blank=False,default=0)

    def __str__(self) -> str:
        return self.fullname


class ResaleCar(models.Model):
    vehicle_identification_number = models.CharField(max_length=50,primary_key=True)
    previous_owner = models.ForeignKey(to=PreviousOwner,on_delete=models.DO_NOTHING)
    car_detail = models.OneToOneField(to=ResaleCarDetail,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.vehicle_identification_number}<=>{self.previous_owner.fullname}"
    
    
    
    