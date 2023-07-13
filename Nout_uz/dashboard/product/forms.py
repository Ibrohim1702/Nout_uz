from django import forms
from Tg_Nout_uz.models import Product


class ProductFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'



