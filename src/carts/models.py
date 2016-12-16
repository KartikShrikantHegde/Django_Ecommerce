from django.conf import settings
from django.db import models

from products.models import Variations


# Create your models here.
from pip._vendor.requests.compat import str


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variations)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.item.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variations, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.id)
