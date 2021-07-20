from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from Account.models import CustomUser
from django.http.response import HttpResponse, JsonResponse
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
                        return redirect('account')
                else:
                    messages.warning(request, f'Invalid Credentials')
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'login_data': login_data})

            else:
                user = authenticate(
                    request, phone=login_phone_or_email, password=login_password)
                if user != None:
                    user_login(request, user)
                    return redirect('account')

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
                            return redirect('account')

            else:
                messages.warning(request, f'Enter a valid phone number')
                return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data})
    return render(request, 'Account/login_or_signup.html', {'title': 'Login'})


def logout(request):
    user_logout(request)
    return redirect('login')


@csrf_exempt
@login_required
def account(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if(name and email and phone):
            similar_email = len(CustomUser.objects.filter(email=email))
            similar_phone = len(CustomUser.objects.filter(phone=phone))
            if(validate_phone(phone)):
                # email received and current user email not same and there are other objects with same email
                if(request.user.email != email and similar_email != 0):
                    return JsonResponse({'message': 'Email Already in Use', 'success': False})
                if(request.user.phone != phone and similar_phone != 0):
                    return JsonResponse({'message': 'Phone Already in Use', 'success': False})
                request.user.email = email
                request.user.phone = phone
                request.user.name = name
                request.user.save()
                print('{}-{}-{}'.format(request.user.email,
                                        request.user.name, request.user.phone))
                return JsonResponse({'message': 'Profile Updated', 'success': True})
            else:
                return JsonResponse({'message': 'Invalid Phone', 'success': False})
        else:
            return JsonResponse({'message': 'Enter all details', 'success': False})
    return render(request, 'Account/myaccount.html', {'title': request.user.name})
