from django.db import models

class ContactDB(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserDB(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartDB(models.Model):
    username = models.CharField(max_length=100,null=True,blank=True)
    ProductName = models.CharField(max_length=100,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    TotalPrice = models.IntegerField(null=True,blank=True)
    Prod_Image = models.ImageField(upload_to="Cart Images",null=True,blank=True)

class OrderDB(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    pin = models.IntegerField(null=True,blank=True)
    total_price = models.IntegerField(null=True,blank=True)
    message = models.CharField(max_length=100,null=True,blank=True)

class Newsletter(models.Model):
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


