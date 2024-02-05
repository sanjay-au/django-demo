from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from shop.models import Product
# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE)
    user=models.ForeignKey(User,on_delete=CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name
    def subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    address=models.TextField()
    phone=models.IntegerField()
    order_status=models.CharField(default='Pending',max_length=20)
    delivery_status=models.CharField(default='Pending',max_length=20)
    order_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Account(models.Model):
    acctnum=models.CharField(max_length=20)
    accttype=models.CharField(max_length=20)
    amount=models.IntegerField()
    def __str__(self):
        return self.acctnum
