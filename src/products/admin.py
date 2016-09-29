from django.contrib import admin

# Register your models here.

from .models import Product,Variations, ProductImage

admin.site.register(Product)

admin.site.register(Variations)

admin.site.register(ProductImage)