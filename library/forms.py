from django import forms
from .models import MainBooks, Category


class MainBooksForm(forms.ModelForm):
    class Meta:
        model = MainBooks
        fields = '__all__'
        exclude = ['auther']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
