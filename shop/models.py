from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator , MaxValueValidator

class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) :
        return self.name

class customer(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=20)
    def __str__(self) :
        return f'{self.first_name} {self.last_name}'



class Profile(models.Model):
    user=models.OneToOneField(User,on_delete = models.CASCADE)
    date_modified=models.DateTimeField(User,auto_now = True)
    phone=models.CharField(max_length=25 , blank=True)
    address1=models.CharField(max_length=250 , blank=True)
    address2=models.CharField(max_length=250 , blank=True)
    city=models.CharField(max_length=25 , blank=True)
    state=models.CharField(max_length=25 , blank=True)
    zipcode=models.CharField(max_length=25 , blank=True)
    country=models.CharField(max_length=25 , blank=True)
    old_cart=models.CharField(max_length=200, blank=True, null=True)
    def __str__(self) :
        return self.user.username



def create_profile(sender,instance,created,**kwargs):
     if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        

post_save.connect(create_profile,sender=User)



class Product(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=500,default='',blank=True , null=True)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=12)
    category=models.ForeignKey(Category , on_delete=models.CASCADE,default=1)
    picture=models.ImageField(upload_to='upload/product')
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=12)
    star=models.IntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0)])
    def __str__(self) :
        return self.name



class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    customer=models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(default='',max_length=50, blank=True)
    phone=models.CharField(max_length=20,blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def __str__(self) :
        return self.product

