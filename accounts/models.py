from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank = True ,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(default = 'profile1.png',null= True,blank = True)
    date_creation = models.DateField(auto_now_add=True,null=True)


    def __str__(self) -> str:
        return self.name




class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)


    def __str__(self) -> str:
        return self.name



class Product(models.Model):
    CATEGORY =(
        ("Indoor","Indoor"),
        ("Out Door","Out Door"),
    )
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True,choices=CATEGORY)
    description = models.CharField(max_length=200, null=True,blank=True)
    date_creation = models.DateField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)



    def __str__(self) -> str:
        return self.name





class Order(models.Model):
    STATUS = (
        ("Pending","Pending"),
        ("Out for delivered", "Out for delivered"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(Customer,related_name="orders",null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="orders", null=True, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100, null=True,choices=STATUS)
    note = models.CharField(max_length=20,null=True)
