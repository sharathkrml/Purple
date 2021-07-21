
from django.urls import path
from .views import cart, getcart
urlpatterns = [
    path('cart/', cart, name='cart'),
    path('getcart/', getcart, name='getcart'),
]
