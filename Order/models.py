from django.db import models
from Account.models import CustomUser, Address
from Product.models import Product
# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField()
