from django.core.paginator import Paginator
from django.db.models.fields import CommaSeparatedIntegerField
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
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


@csrf_exempt
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    p = Paginator(products, 12)
    if(request.method == 'POST'):
        page_no = request.POST.get('page_no')
        products_of_that_page = p.page(page_no).object_list
        products_dict = {}
        key = 0
        for single_product in products_of_that_page:
            key = key+1
            single_product_dict = {}
            single_product_dict['name'] = single_product.name
            single_product_dict['price_new'] = single_product.price_new
            single_product_dict['imageurl'] = single_product.imageurl
            single_product_dict['image_slug'] = single_product.slug
            products_dict[key] = single_product_dict
        return JsonResponse(products_dict)
    return render(request, 'Product/category.html', {'slug': slug, 'title': category.name, 'total_page_no': p.num_pages})


def home(request):
    return render(request, 'Product/index.html')


def contactus(request):
    return render(request, 'Product/contactus.html')
