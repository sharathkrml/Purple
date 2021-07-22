from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart, Product
from django.views.decorators.csrf import csrf_exempt
from Product.views import Navbar
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
