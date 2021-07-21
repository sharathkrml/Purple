import random
from django.core.paginator import Paginator
from django.db.models.fields import CommaSeparatedIntegerField
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
# Create your views here.
OCCASIONAL = ['Birthday',
              'Anniversary',
              'New Year',
              'Christmas',
              'Valentines',
              'Friendship Day']
CATEGORIES = ['Cakes',
              'Flowers',
              'Jewellery',
              'Plants',
              'Sweets',
              'Perfumes',
              'Personalised']
Navbar = {'CATEGORIES': CATEGORIES, 'OCCASIONAL': OCCASIONAL}


def productListtodict(product_list):
    products_dict = {}
    key = 0
    for single_product in product_list:
        key = key+1
        single_product_dict = {}
        single_product_dict['name'] = single_product.name
        single_product_dict['price_new'] = single_product.price_new
        single_product_dict['imageurl'] = single_product.imageurl
        single_product_dict['pro_slug'] = single_product.slug
        products_dict[key] = single_product_dict
    return(products_dict)


def getRandomProduct(number):
    product_list = list(Product.objects.all())
    output_list = []
    for i in range(number):
        random_product = random.choice(product_list)
        output_list.append(random_product)
        product_list.remove(random_product)
    return(output_list)


def product(request, slug):
    print(Product.objects.filter(slug=slug))
    product = Product.objects.filter(slug=slug).first()
    if(product.price != product.price_new):
        product_dict = {'name': product.name, 'description': product.description,
                        'category': product.category, 'imageurl': product.imageurl,
                        'price': product.price, 'price_new': product.price_new}
    else:
        product_dict = {'id': product.id, 'name': product.name, 'description': product.description,
                        'category': product.category, 'imageurl': product.imageurl,
                        'price': product.price}
    Related_Products_dict = productListtodict(getRandomProduct(4))
    return render(request, 'Product/product.html', {'Navbar': Navbar,
                                                    'title': product.name,
                                                    'product_dict': product_dict,
                                                    'Related_Products_dict': Related_Products_dict})


@csrf_exempt
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    p = Paginator(products, 12)
    if(request.method == 'POST'):
        page_no = request.POST.get('page_no')
        products_of_that_page = p.page(page_no).object_list
        return JsonResponse(productListtodict(products_of_that_page))
    return render(request, 'Product/category.html', {'Navbar': Navbar, 'slug': slug, 'title': category.name, 'total_page_no': p.num_pages})


def home(request):
    products_dict = {}
    key = 0
    Featured_Products_dict = productListtodict(getRandomProduct(4))
    Latest_Products_dict1 = productListtodict(getRandomProduct(4))
    Latest_Products_dict2 = productListtodict(getRandomProduct(4))
    return render(request, 'Product/index.html', {'Navbar': Navbar,
                                                  'Featured_Products_dict': Featured_Products_dict,
                                                  'Latest_Products_dict1': Latest_Products_dict1,
                                                  'Latest_Products_dict2': Latest_Products_dict2})


def contactus(request):
    return render(request, 'Product/contactus.html')
