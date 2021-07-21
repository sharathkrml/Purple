
from django.urls import path
from .views import product, category, home, contactus
urlpatterns = [
    path('product/<slug>/', product, name='product'),
    path('product/', product, name='product_url'),
    path('category/<slug>', category, name='category'),
    path('category/', category, name='category_url'),
    path('', home, name='home'),
    path('contactus/', contactus, name='contactus')
]
