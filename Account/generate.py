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
    Cat = Category.objects.create(name=k)
    print(Cat)

for i in path_list:
    csv_path = os.path.join(os.path.dirname(__file__), i)
    All = pd.read_csv(csv_path)
    for j in range(All.shape[0]):
        category = i[:-4]
        Cat = Category.objects.filter(name=category).first()
        p = Product(
            category=Cat,
            name=All['name'][j],
            description=All['description'][j],
            imageurl=All['imageurl'][j],
            price=All['price'][j],
            price_new=All['price_new'][j])
        p.save()
        print(p)
