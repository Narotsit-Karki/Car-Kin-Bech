from django.db import models
from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from common.models import KinBechUser
from django.urls import reverse

from faker import Faker
import pandas as pd
cleaned_data = pd.read_csv('model_data/car_resale_price_cleaned.csv')
# original_data = pd.read_csv('model_data/car_resale_prices_origina.csv')
# Create your models here.
class GeneralDetails:
    
    generator = Faker(['en_IN'])
    
    @classmethod
    def generate_owner_name(cls) -> str:
        return cls.generator.name()
    @classmethod
    def generate_owner_address(cls) -> str:
        return cls.generator.address()
    @classmethod
    def generate_owner_phone_number(cls) -> str:
        return cls.generator.phone_number()
    
class ResaleCarDetail(BaseModel):
    Nan = 'Nan'  
    BRAND_TYPE = ((brand,brand) for brand in cleaned_data['Car_company'].unique())
    INSURANCE_TYPE = ((insurance,insurance) for insurance in cleaned_data['Insurance_type'].unique())
    ENGINE_TYPE = ((engine,engine) for engine in cleaned_data['Fuel_type'].unique())
    TRANSMISSION_TYPE = ((transmission,transmission) for transmission in cleaned_data['Transmission_type'].unique())
    MODEL_TYPE = ((model,model) for model in cleaned_data['Car_model'].unique())
    BODY_TYPE = ((body,body) for body in cleaned_data['Body_type'].unique())
    CITY = ((city,city) for city in cleaned_data['City'].unique())
    OWNER_TYPE = ((owner , owner ) for owner in cleaned_data['Owner_type'].unique())

    brand = models.CharField(max_length=100,choices=BRAND_TYPE,default=Nan)
    model = models.CharField(max_length=255,choices = MODEL_TYPE,default = Nan)
    insurance_type = models.CharField(max_length=200,choices=INSURANCE_TYPE,default=Nan)
    engine_type = models.CharField(max_length=100 , choices=ENGINE_TYPE,default=Nan)
    engine_capacity = models.IntegerField(default=0)
    kms_driven = models.BigIntegerField()
    no_of_seat = models.IntegerField(null = False,blank=False)
    transmission_type = models.CharField(max_length=100 , choices=TRANSMISSION_TYPE,default=Nan)
    mileage = models.FloatField()
    registered_year = models.IntegerField()
    max_power = models.FloatField()
    body_type = models.CharField(choices=BODY_TYPE,default=Nan,max_length=100)
    city = models.CharField(choices=CITY,default=Nan,max_length=50)
    owner_type = models.CharField(max_length=100,choices=OWNER_TYPE,default=Nan)
    extra_info = models.CharField(max_length=500,null=False,blank=False,default=Nan)
   
    def __str__(self):
        return f"{self.brand} {self.model} {self.registered_year}"

    @property
    def km_driven(self):
        return (format (self.kms_driven, ',d')) 

class PreviousOwner(BaseModel):
    fullname = models.CharField(max_length=255,null=False,blank=False,default=GeneralDetails.generate_owner_name)
    contact_phone = models.BigIntegerField(null=False,blank=False,default=GeneralDetails.generate_owner_phone_number)
    address = models.TextField(default=GeneralDetails.generate_owner_address)
    
    def __str__(self) -> str:
        return self.fullname


class ResaleCar(models.Model):
   
    
    vehicle_identification_number = models.CharField(max_length=50,primary_key=True)
    previous_owner = models.ForeignKey(to=PreviousOwner,on_delete=models.DO_NOTHING,null=True,blank=True)
    car_detail = models.OneToOneField(to=ResaleCarDetail,on_delete=models.CASCADE,null=True,blank=True)
    price = models.FloatField(null=False,blank=False)
    
    @property
    def fullname(self):
        return f"{self.car_detail.registered_year} {self.car_detail.brand} {self.car_detail.model}"
    
    # converting lakh price to full decimal digit
    @property
    def full_price(self):
        price  = self.price * 1e6
        return (format(int(price),',d'))
    
    def get_absolute_url(self):
        return reverse('car-detail',args=[str(self.vehicle_identification_number)])

    
    def __str__(self) -> str:
        return f"{self.vehicle_identification_number}<=>{self.previous_owner.fullname}"
    

class WishList(BaseModel):
    user = models.ForeignKey(to=KinBechUser,on_delete=models.CASCADE)
    car = models.ForeignKey(to=ResaleCar,on_delete=models.CASCADE)

    def _str__(self) -> str:
        return f"{self.user.username} {self.car.vehicle_identification_number}"
    

# saves previous owner and car_detail after saving new ResaleCar object
@receiver(pre_save,sender = ResaleCar)
def save_previous_owner_and_car_detail(sender,instance,**kwargs):
    # extracting car details from VIN from cleaned resale data
    car_detail_extracted = cleaned_data.loc[cleaned_data['VIN'] == instance.vehicle_identification_number]
    previous_owner = PreviousOwner.objects.create()
 
    car_detail = ResaleCarDetail.objects.create(
        brand = car_detail_extracted["Car_company"].values[0],
        model = car_detail_extracted["Car_model"].values[0],
        insurance_type = car_detail_extracted["Insurance_type"].values[0],
        engine_type = car_detail_extracted["Fuel_type"].values[0],
        engine_capacity = int(car_detail_extracted["Engine_capacity"].values[0]), 
        kms_driven = car_detail_extracted["KM_driven"].values[0],
        no_of_seat = car_detail_extracted["Seats"].values[0],
        transmission_type = car_detail_extracted["Transmission_type"].values[0],
        mileage = car_detail_extracted["Mileage"].values[0], 
        registered_year = car_detail_extracted["Registered_year"].values[0],
        max_power = car_detail_extracted["Max_power_bhp"].values[0],
        body_type = car_detail_extracted["Body_type"].values[0],
        city = car_detail_extracted["City"].values[0],
        owner_type = car_detail_extracted["Owner_type"].values[0],
        extra_info = car_detail_extracted["Extra_info"].values[0]
    )

    previous_owner.save()
    car_detail.save()

    instance.previous_owner = previous_owner
    instance.car_detail = car_detail


    
    