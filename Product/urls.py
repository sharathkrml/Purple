
from django.urls import path
from .views import product
urlpatterns = [
    path('product/<slug>/', product, name='product'),
    path('product/', product, name='product_url'),
]
