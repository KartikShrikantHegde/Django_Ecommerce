from django.contrib import admin

# Register your models here.

from .models import Product, Variations, ProductImage, Category, ProductFeatured


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0           # Just one inline field not more
    max_num = 10


class VariationInline(admin.TabularInline):
    model = Variations
    extra = 0
    max_num = 10  # The no variations allowed per product


# To manage products in admin page
class ProductAdmin(admin.ModelAdmin):
    # Here unicode represents the product itself, price ll be shown against it in admin page
    list_display = ['__unicode__', 'price']
    inlines = [
        ProductImageInline,
        VariationInline,
    ]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

# this can be commented as variation is added as model in inline
# admin.site.register(Variations)

# admin.site.register(ProductImage)

admin.site.register(Category)

admin.site.register(ProductFeatured)
