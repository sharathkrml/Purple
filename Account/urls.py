
from django.urls import path
from .views import login, logout, account, address, edit_or_delete_address
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', account, name='account'),
    path('address/', address, name='address'),
    path('editaddress/', edit_or_delete_address, name='editaddress'),
]
