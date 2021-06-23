
from django.urls import path
from .views import addaddress, login, signup, logout
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
]
