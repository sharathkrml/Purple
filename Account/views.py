from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from Account.models import CustomUser
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
# Create your views here.


def validate_phone(s):
    num_pattern = re.compile((r"^[6-9]\d{9}$"))
    return num_pattern.match(s)


@csrf_exempt
def login(request):
    if(request.method == 'POST'):
        # login
        login_phone_or_email = request.POST.get('login_phone_or_email')
        login_password = request.POST.get('login_password')
        login_data = {'login_phone_or_email': login_phone_or_email}
        if(login_phone_or_email and login_password):
            if('@' in login_phone_or_email):
                user = CustomUser.objects.get(email=login_phone_or_email)
                if user != None:
                    if(user.check_password(login_password)):
                        user_login(request, user)
                else:
                    messages.warning(request, f'Invalid Credentials')
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'login_data': login_data})

            else:
                user = authenticate(
                    request, phone=login_phone_or_email, password=login_password)
                if user != None:
                    user_login(request, user)
                else:
                    messages.warning(request, f'Invalid Credentials')
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'login_data': login_data})

        # register
        register_username = request.POST.get('register_username')
        register_phoneno = request.POST.get('register_phoneno')
        register_email = request.POST.get('register_email')
        register_password = request.POST.get('register_password')
        register_data = {'register_username': register_username,
                         'register_phoneno': register_phoneno, 'register_email': register_email}
        if(register_username and register_phoneno and register_email and register_password):
            if(validate_phone(register_phoneno)):
                try:
                    validate_email(register_email)
                except ValidationError as e:
                    message = list(e)
                    messages.warning(request, message[0])
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
                else:
                    if(CustomUser.objects.filter(email=register_email)):
                        messages.warning(request, f'Email already Exist')
                        return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
                    elif(CustomUser.objects.filter(phone=register_phoneno)):
                        messages.warning(request, f'Phone already Exist')
                        return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
                    else:
                        try:
                            validate_password(register_password)
                        except ValidationError as e:
                            message = list(e)
                            messages.warning(request, message[0])
                            return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
                        else:
                            user = CustomUser(
                                email=register_email, name=register_username, phone=register_phoneno)
                            user.set_password(register_password)
                            user.save()
                            user_login(request, user)
                            return redirect('login')

            else:
                messages.warning(request, f'Enter a valid phone number')
                return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
    return render(request, 'Account/login_or_signup.html', {'title': 'Login'})


def logout(request):
    user_logout(request)
    return redirect('login')
