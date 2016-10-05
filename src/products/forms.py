from django import forms

from django.forms.models import modelformset_factory
from .models import Variations

class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variations
        fields = [
            "title",
            "price",
            "sale_price",
            "inventory",
            "active"
        ]


VariationInventoryFormSet = modelformset_factory(Variations, form=VariationInventoryForm,extra=0)