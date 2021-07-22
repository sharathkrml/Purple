
from django.urls import path
from .views import login, logout, account, address, edit_or_delete_address, forgot, verify, reset
urlpatterns = [
    path('forgot/', forgot, name='forgot'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', account, name='account'),
    path('address/', address, name='address'),
    path('editaddress/', edit_or_delete_address, name='editaddress'),
    path('forgot/', forgot, name='forgot'),
    path('verify/', verify, name='verify'),
    path('reset/', reset, name='reset')
]
