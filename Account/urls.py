
from django.urls import path
from .views import login, logout, account
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', account, name='account'),
]
