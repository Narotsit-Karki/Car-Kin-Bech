from django.urls import path
from .views import WishListView,add_or_remove_wishlist,ResaleCarCatalogView,ResaleCarDetailView,home




urlpatterns = [
    path("",home,name = "home"),
    path('buy-car',ResaleCarCatalogView.as_view(),name='car-list-catalog'),
    path('car-detail/<pk>', ResaleCarDetailView.as_view(),name = 'car-detail'),
    path('wishlist',WishListView.as_view(),name = 'wishlist'),
    path('add-remove-wishlist',add_or_remove_wishlist,name = 'add_or_remove_wishlist')
]