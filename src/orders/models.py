from django.db.models.signals import pre_save,post_save
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db import models
import math
ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('Paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),

)
# Create your models here.
class Order(models.Model):
    order_id=models.CharField(max_length=120,blank=True)
    # billing_profile=
    # shipping_address=
    # billing_address=
    cart=models.ForeignKey(Cart)
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total=models.DecimalField(default=50,max_digits=100,decimal_places=2)
    total=models.DecimalField(default=0,max_digits=100,decimal_places=2)

    def __str__(self):
        return self.order_id
    
    def update_total(self):
        cart_total=self.cart.total
        shippping_total=self.shipping_total
        new_total=math.fsum([cart_total+shippping_total])
        formatted_total=format(new_total,'.2f')
        self.total =new_total
        self.save()
        return

def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    
pre_save.connect(pre_save_create_order_id,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id 
        qs=Order.objects.filter(cart__id=cart_id)
        if qs.exists() and qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)

