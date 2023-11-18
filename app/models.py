from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name    
    
class Product(models.Model):
    Availability = (('In Stock','In Stock'),('Out of Stock','Out of Stock'))

    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='product')
    sub_category = models.ForeignKey("Sub_category", on_delete=models.CASCADE, related_name='product')
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name='product')
    image = models.ImageField(upload_to='ecommerce/prod_img')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    Availability = models.CharField(max_length=150, choices=Availability, default='1')

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False, blank=False)
    subject = models.CharField(max_length=150, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    image = models.ImageField(upload_to='ecom/order/image')
    product = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
    price = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.today)
    total = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.product
    




