from typing import Any
from django.core.management import BaseCommand
from resale_store_module.models import ResaleCar
from resale_store_module.models import cleaned_data

# Seeding the data base with our cleaned csv data
class Command(BaseCommand):
    help = "Loads data from our model data to datbase"

    def handle(self, *args: Any, **options: Any) -> str | None:
        if ResaleCar.objects.exists():
            print('Data base already seeded')
            return 
        
        print("[*] Loading Resale data to Database")

        for index , row in cleaned_data.head(10).iterrows():
            resale_car = ResaleCar.objects.create(
                vehicle_identification_number = row["VIN"],
                price = row["Resale_price_lakh"]
            )
            resale_car.save()
