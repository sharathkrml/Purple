from django.conf import settings
from django.core.mail import send_mail
import pyotp
import base64
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from Account.models import Address, CustomUser
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from Product.views import Navbar
# Create your views here.
'''pastecode here'''

from Product.models import Category, Product
# Create your views here.

import os
import pandas as pd
import numpy as np
path_list = ['Anniversary.csv',
             'Birthday.csv',
             'Cakes.csv',
             'Christmas.csv',
             'Flowers.csv',
             'Friendship Day.csv',
             'Jewellery.csv',
             'New Year.csv',
             'Perfumes.csv',
             'Personalised.csv',
             'Plants.csv',
             'Sweets.csv',
             'Valentines.csv']
#csv_path = os.path.join(os.path.dirname(__file__), 'All.csv')
#All = pd.read_csv(csv_path)
#rows = All.shape[0]
# Create your views here.
# int(a.lstrip('Rs').replace(',',''))
category_list = ['Birthday',
                 'Anniversary',
                 'New Year',
                 'Christmas',
                 'Valentines',
                 'Friendship Day',
                 'Personalised',
                 'Flowers',
                 'Cakes',
                 'Plants',
                 'Jewellery',
                 'Perfumes',
                 'Sweets']
for k in category_list:
    if(len(Category.objects.filter(name=k))==0):
        Cat = Category.objects.create(name=k)
        print(Cat)

for i in path_list:
    csv_path = os.path.join(os.path.dirname(__file__), i)
    All = pd.read_csv(csv_path)
    for j in range(All.shape[0]):
        category = i[:-4]
        Cat = Category.objects.filter(name=category).first()
        if(len(Product.objects.filter(name=All['name'][j]))==0):
            p = Product(
                category=Cat,
                name=All['name'][j],
                description=All['description'][j],
                imageurl=All['imageurl'][j],
                price=All['price'][j],
                price_new=All['price_new'][j])
            p.save()
            print(p)

''''''
key = random.randint(1, 999999)


@csrf_exempt
def forgot(request):
    if(request.POST.get('userdata')):
        key2 = random.randint(1, 999999)
        request.session['key2'] = key2
        userdata = request.POST.get('userdata')
        if('@' in userdata):
            user = CustomUser.objects.filter(email=userdata).first()
        else:
            user = CustomUser.objects.filter(phone=userdata).first()

        if(user == None):
            messages.warning(request, f'No Such User')
            return redirect('forgot')
        else:
            request.session['email'] = user.email
            return redirect('verify')
    return render(request, 'Account/forgotPassword.html', {'title': 'Forgot Password'})


@csrf_exempt
def verify(request):
    totp = pyotp.HOTP('base32secret3232')
    key2 = request.session['key2']
    send_mail('Purple password reset', 'Purple password reset otp='+str(totp.at(key2)),
              settings.EMAIL_HOST_USER, [request.session['email']], fail_silently=False)
    print(totp.at(key2))
    if request.method == "POST":
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        otp = request.POST['Otpinput']
        if(totp.verify(otp, key2)):
            request.session['otp'] = otp
            return redirect('reset')
        else:
            messages.warning(request, f'Invalid otp')
            return redirect('verify')
    return render(request, 'Account/verifyOTP.html', {'title': 'Verify OTP', 'Navbar': Navbar})


@csrf_exempt
def reset(request):
    if(request.method == 'POST'):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if(password2 == password1):
            try:
                validate_password(password1)
            except ValidationError as e:
                message = list(e)
                messages.warning(request, message[0])
            else:
                totp = pyotp.HOTP('base32secret3232')
                key2 = request.session['key2']
                otp = request.session['otp']
                if(totp.verify(otp, key2)):
                    user = CustomUser.objects.filter(
                        email=request.session.get('email')).first()
                    user.set_password(password1)
                    user.save()
                    messages.success(request, f'Succesfully changed password')
                    return redirect('login')
                else:
                    messages.warning(request, f'Passwords dont match')
                    return redirect('reset')
    return render(request, 'Account/resetPassword.html', {'title': 'Reset Password', 'Navbar': Navbar})


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
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'login_data': login_data, 'Navbar': Navbar})

            else:
                user = authenticate(
                    request, phone=login_phone_or_email, password=login_password)
                if user != None:
                    user_login(request, user)
                    return redirect('home')

                else:
                    messages.warning(request, f'Invalid Credentials')
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'login_data': login_data, 'Navbar': Navbar})

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
                    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data, 'Navbar': Navbar})
                else:
                    if(CustomUser.objects.filter(email=register_email)):
                        messages.warning(request, f'Email already Exist')
                        return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data, 'Navbar': Navbar})
                    elif(CustomUser.objects.filter(phone=register_phoneno)):
                        messages.warning(request, f'Phone already Exist')
                        return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data, 'Navbar': Navbar})
                    else:
                        try:
                            validate_password(register_password)
                        except ValidationError as e:
                            message = list(e)
                            messages.warning(request, message[0])
                            return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data, 'Navbar': Navbar})
                        else:
                            user = CustomUser(
                                email=register_email, name=register_username, phone=register_phoneno)
                            user.set_password(register_password)
                            user.save()
                            user_login(request, user)
                            return redirect('account')

            else:
                messages.warning(request, f'Enter a valid phone number')
                return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'register_data': register_data, 'Navbar': Navbar})
    return render(request, 'Account/login_or_signup.html', {'title': 'Login', 'Navbar': Navbar})


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
    return render(request, 'Account/myaccount.html', {'title': request.user.name.title(), 'Navbar': Navbar})


@csrf_exempt
def address(request):
    if(request.method == 'POST'):
        # add new address of current user
        print(request.POST)
        if(request.POST.get('fullname') and request.POST.get('mobile_no') and request.POST.get('state') and request.POST.get('locality_details') and request.POST.get('pin_code') and request.POST.get('building_details')):
            new_address = Address(
                user=request.user,
                fullname=request.POST.get('fullname'),
                mobile_no=request.POST.get('mobile_no'),
                pin_code=request.POST.get('pin_code'),
                building_details=request.POST.get('building_details'),
                locality_details=request.POST.get('locality_details'),
                state=request.POST.get('state')
            )
            new_address.save()
            return JsonResponse({'message': "Address Added", 'success': True})
    addresses = Address.objects.filter(user=request.user)
    print(addresses)
    address_dict = {}
    address_counter = 0
    for single_address in addresses:
        single_address_dict = {}
        address_counter = address_counter+1
        single_address_dict['id'] = single_address.id
        single_address_dict['fullname'] = single_address.fullname
        single_address_dict['mobile_no'] = single_address.mobile_no
        single_address_dict['pin_code'] = single_address.pin_code
        single_address_dict['building_details'] = single_address.building_details
        single_address_dict['locality_details'] = single_address.locality_details
        single_address_dict['state'] = single_address.state
        address_dict[address_counter] = single_address_dict
    return JsonResponse(address_dict)


@csrf_exempt
def edit_or_delete_address(request):
    if(request.POST.get('delete_id')):
        delete_address = Address.objects.get(pk=request.POST.get('delete_id'))
        delete_address.delete()
        return JsonResponse({'message': "Address Deleted", 'success': True})

    if(request.POST.get('edit_id')):
        edit_address = Address.objects.get(pk=request.POST.get('edit_id'))
        edit_address.fullname = request.POST.get('fullname')
        edit_address.mobile_no = request.POST.get('mobile_no')
        edit_address.pin_code = request.POST.get('pin_code')
        edit_address.building_details = request.POST.get('building_details')
        edit_address.locality_details = request.POST.get('locality_details')
        edit_address.state = request.POST.get('state')
        edit_address.save()
        return JsonResponse({'message': "Address Edited", 'success': True})
    id = request.GET.get('id')
    address = Address.objects.get(pk=id)
    data = {
        'fullname': address.fullname,
        'mobile_no': address.mobile_no,
        'pin_code': address.pin_code,
        'building_details': address.building_details,
        'locality_details': address.locality_details,
        'state': address.state,
    }
    return JsonResponse(data)
