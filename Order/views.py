from .models import Order
from Account.models import Address
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart, Product
from django.views.decorators.csrf import csrf_exempt
from Product.views import Navbar, product
# Create your views here.


@csrf_exempt
@login_required
def getcart(request):
    if(request.method == 'GET'):
        cart_items_list = Cart.objects.filter(user=request.user, ordered=False)
        cart_items_dict = {}
        k = 0
        for cart_item in cart_items_list:
            k = k+1
            cart_item_dict = {
                'id': cart_item.id,
                'name':  cart_item.product.name,
                'price': cart_item.product.price_new,
                'imageurl': cart_item.product.imageurl,
                'quantity': cart_item.quantity,
                'total': cart_item.quantity*cart_item.product.price_new
            }
            cart_items_dict[k] = cart_item_dict
        return JsonResponse(cart_items_dict)


@csrf_exempt
@login_required
def cart(request):
    if(request.user.is_authenticated):
        if(request.POST.get('product_id')):  # add to cart
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            quantity = request.POST.get('quantity')
            if(len(Cart.objects.filter(product=product, user=request.user, ordered=False)) == 0):
                # checks if there is an entry,if no
                new = Cart(user=request.user,
                           product=product,
                           quantity=quantity, ordered=False)
                new.save()
            else:
                old_object = Cart.objects.filter(
                    product=product, user_id=request.user, ordered=False).first()
                old_object.quantity = old_object.quantity + int(quantity)
                old_object.save()
            return JsonResponse({'message': 'Item Added To Cart', 'success': True})
        if(request.POST.get('delete_id')):  # delete from cart
            cart_object = Cart.objects.get(pk=request.POST['delete_id'])
            cart_object.delete()
            return JsonResponse({'message': 'Item Deleted From Cart', 'success': True})
        if(request.POST.get('update_id')):  # delete from cart
            quantity = request.POST.get('quantity')
            cart_object = Cart.objects.get(pk=request.POST['update_id'])
            cart_object.quantity = quantity
            cart_object.save()
            return JsonResponse({'success': True})

    return render(request, 'Order/cart.html', {'title': 'Cart', 'Navbar': Navbar})


@csrf_exempt
@login_required
def checkout(request):
    if(request.method == 'POST'):
        id = request.POST.get('id')
        address = Address.objects.get(pk=id)
        cart = Cart.objects.filter(
            user_id=request.user, ordered=False)
        total = 0
        for i in cart:
            total = total+i.product.price_new
        print(total)
        order = Order(
            user=request.user,
            address=address,
            delivery_status='YET TO BE DISPATCHED',
            total_price=total
        )
        order.save()
        order.cart.set(cart)
        print(order)
        for i in cart:
            i.ordered = True
            i.save()
        return JsonResponse({'message': 'Checkout Successful', 'success': True})

    return render(request, 'Order/checkout.html', {'title': 'Checkout', 'Navbar': Navbar})


@csrf_exempt
def getorderdetails(request):
    orders = Order.objects.filter(user=request.user)
    orders_dict = {}
    for order in orders:
        address = order.address.fullname + " "+order.address.building_details + \
            " "+order.address.locality_details + " "+order.address.pin_code
        total = order.total_price
        status = order.delivery_status
        products_dict = {}
        key = 1
        for cart in order.cart.all():
            quantity = cart.quantity
            name = cart.product.name
            product_price = quantity*cart.product.price_new
            products_dict[key] = {'quantity': quantity,
                                  'name': name,
                                  'product_price': product_price}
            key = key+1
        orders_dict[order.id] = {
            'address': address,
            'total': total,
            'status': status,
            'products_dict': products_dict
        }
    return JsonResponse(orders_dict)
