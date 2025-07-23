from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import post_save
from django.utils import timezone


class ShippingAddress(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    shipping_full_name=models.CharField(max_length=250,blank=True)
    shipping_email=models.CharField(max_length=300,blank=True)
    shipping_phone=models.CharField(max_length=25,blank=True)
    shipping_address1=models.CharField(max_length=250,blank=True)
    shipping_address2=models.CharField(max_length=250, blank=True, null=True)
    shipping_city=models.CharField(max_length=25,blank=True)
    shipping_state=models.CharField(max_length=25,blank=True)
    shipping_zipcode=models.CharField(max_length=25,blank=True)
    shipping_country=models.CharField(max_length=25,blank=True)
    


    class Meta:
        verbose_name_plural='Shipping Address'

    def __str__(self):
        
        return f'Shipping address from {self.shipping_full_name}'
    
def create_shipping_user(sender,instance,created,**kwargs):
     if created:
        user_shipping=ShippingAddress(user=instance)
        user_shipping.save()
        

post_save.connect(create_shipping_user,sender=User)


class Order(models.Model):
    status_order=[
    ('Pending','Waiting for payment'),
    ('Processing','Processing'),
    ('Shipped','Order shipped'),
    ('Delivered','Order successfully delivered'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name=models.CharField(max_length=250,blank=True)
    email=models.EmailField(max_length=250)
    shipping_address=models.TextField(max_length=15000)
    amount_paid=models.DecimalField(decimal_places=2,max_digits=12)
    date_ordered=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices=status_order, default='Pending')
    last_update=models.DateTimeField(auto_now=True)

    """ def save(self,*args,**kwargs):
        if self.pk:
            old_status=Order.objects.get(id=self.pk).status

            if old_status!=self.status:
                self.last_update=timezone.now()

        super().save(*args,**kwargs) """





    def __str__(self):
        return f'Order - {self.id}'


class OrderItem(models.Model):

    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(decimal_places=2,max_digits=12)

    def __str__(self):
        if self.user is not None:
            return f'Order Item - {self.id} - for {self.user}'
        else:
            return f'Order Item - {self.id}'

