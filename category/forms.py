from django import forms
from .models import Category


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']

class UpdateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']
