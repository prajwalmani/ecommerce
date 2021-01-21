import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('Paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),

)
# Create your models here.
class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile, 
                cart=cart_obj, 
                active=True, 
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
    
            obj = self.model.objects.create(
                    billing_profile=billing_profile, 
                    cart=cart_obj)
            created = True
        return obj, created
class Order(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id            = models.CharField(max_length=120, blank=True) 
    shipping_address    = models.ForeignKey(Address, related_name="shipping_address",null=True, blank=True)
    billing_address     = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True)
    cart                = models.ForeignKey(Cart)
    status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active              = models.BooleanField(default=True)
    def __str__(self):
        return self.order_id
    
    objects=OrderManager()
    def update_total(self):
        cart_total=self.cart.total
        shippping_total=self.shipping_total
        new_total=math.fsum([cart_total,shippping_total])
        formatted_total=format(new_total,'.2f')
        self.total =new_total
        self.save()
        return

    def check_done(self):
        billing_profile=self.billing_profile
        shippping_address=self.shippping_address
        billing_address=self.billing_address
        total=self.total   
        if billing_profile and shippping_address and billing_address and total>0:
            return True
        return False
    
    def mark_paid(self):
        if self.check_done():
            self.status="paid"
            self.save()
        return self.status
def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)    
    if qs.exists():
        qs.update(active=False )
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

