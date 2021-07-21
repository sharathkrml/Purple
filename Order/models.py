from django.db import models
from Account.models import CustomUser
from Product.models import Product
# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    cart_total_price = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.cart_total_price:
            self.cart_total_price = self.quantity * self.product_id.selling_price
        super(Cart, self).save(*args, **kwargs)
