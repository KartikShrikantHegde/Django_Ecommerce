from django.contrib import admin

# Register your models here.

from .models import Cart, CartItem


# Make the cart items table tabular
class CartItemInline(admin.TabularInline):
    model = CartItem


# define the inliners for the admin
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
