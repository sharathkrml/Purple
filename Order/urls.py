
from django.urls import path
from .views import cart, getcart, checkout
urlpatterns = [
    path('cart/', cart, name='cart'),
    path('getcart/', getcart, name='getcart'),
    path('checkout/', checkout, name='checkout'),
]
