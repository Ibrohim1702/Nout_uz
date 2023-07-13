from django import forms
from Tg_Nout_uz.models import Brands


class BrandsFrom(forms.ModelForm):
    class Meta:
        model = Brands
        fields = '__all__'



