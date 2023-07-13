from django import forms
from Tg_Nout_uz.models import Category


class CategoryFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



