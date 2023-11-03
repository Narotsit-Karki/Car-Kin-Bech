from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404 , redirect
from django.http import request
from .models import WishList,ResaleCar
from django.contrib import messages
from django.views.generic import ListView,DetailView
# Create your views here.
from .models import cleaned_data

class ResaleCarCatalogView(ListView):
    template_name = "resale-car-list.html"
    context_object_name = 'resale_car'
    model = ResaleCar

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['CAR_BRANDS'] = cleaned_data['Car_company'].unique()
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        # get brand choosen from user selection and filter the car brand and send the result
        car_brand = self.request.GET.get('q','')
        if car_brand == '':
            return ResaleCar.objects.all()
        else:
            return ResaleCar.objects.filter(car__car_detail__brand = '')
        
    


class ResaleCarDetailView(DetailView):
    template_name = "resale-car-detail.html"
    context_object_name = 'resale_car'
    model = ResaleCar







class WishListView(ListView):
    template_name = 'wishlist.html'
    context_object_name = 'user_wishlist'
    model = WishList

    def get_queryset(self) -> QuerySet[Any]:
        try:
            return None
            # return self.model.objects.filter(user = self.request.user)
        except Exception:
            return None

def add_or_remove_wishlist(request,vin):
    car = get_object_or_404(ResaleCar,vin = vin)
    whishlist,created = WishList.objects.get_or_create(user = request.user , car = car )
    if not created:
        messages.success(request,message = "added to your wishlist")
        return redirect(request.META['HTTP_REFERER'])
    else:
        whishlist.delete()
        messages.success(request,message = "removed from wishlist")
        return redirect(request.META['HTTP_REFERER'])
    



