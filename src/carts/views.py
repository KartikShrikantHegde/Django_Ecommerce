from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

class CartView(View):
    def get(self,request,*args,**kwargs):
        item = request.GET.get("item")
        qty = request.GET.get("qty")
        print item,qty
        return HttpResponseRedirect("/")
