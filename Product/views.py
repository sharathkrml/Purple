from django.shortcuts import render
from .models import Product
# Create your views here.


def product(request, slug):
    product = Product.objects.get(slug=slug)
    if(product.price != product.price_new):
        product_dict = {'name': product.name, 'description': product.description,
                        'category': product.category, 'imageurl': product.imageurl,
                        'price': product.price, 'price_new': product.price_new}
    else:
        product_dict = {'name': product.name, 'description': product.description,
                        'category': product.category, 'imageurl': product.imageurl,
                        'price': product.price}
    return render(request, 'Product/product.html', {'title': product.name, 'product_dict': product_dict})
