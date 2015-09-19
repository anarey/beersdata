from django import forms
from .models import Beer, Recipe, Ingredient, Purchase


class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = '__all__'

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('ingredient', 'quantity')

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = '__all__'

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = '__all__'
