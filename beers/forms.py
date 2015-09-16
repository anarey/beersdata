from django import forms
from .models import Beer, Recipe

class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = '__all__'

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('ingredient', 'quantity')
