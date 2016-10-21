from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.

from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variations, Category


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args,**kwargs)
        obj = self.get_object()
        print obj
        product_set = obj.product_set.all()
        print product_set
        default_products = obj.default_category.all()
        products = ( product_set | default_products ).distinct()   # to avoid the duplicate when queryset are combined
        context["products"] = products
        return context

# Provides a view list

class VariationListView(StaffRequiredMixin, ListView):
    model = Variations
    queryset = Variations.objects.all()

    # This is the default method overriding in Django Productlistview

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variations.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                # if new_item.title:
                product_pk = self.kwargs.get("pk")
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()

            messages.success(request, "Your inventory and pricing has been updated.")
            return redirect("products")
        raise Http404




class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    # This is the default method overriding in Django Productlistview

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context

    # Search functionality for multiple items

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


class ProductDetailView(DetailView):
    model = Product

    # override the default get contect method
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        instance = self.get_object()
        context["related"] = Product.objects.get_related(instance).order_by("?")[:6]    # list only 6 related products
        return context

def product_detail_view_func(request, id):
    # product_instance = Product.objects.get(id=id)
    # try:
    #     product_instance = Product.objects.get(id=id)
    # except Product.DoesNotExist:
    #     raise Http404
    # except:
    #     raise Http404

    product_instance = get_object_or_404(Product, id=id)
    template = "products/product_detail.html"
    context = {
        "object": product_instance
    }
    return render(request, template, context)
