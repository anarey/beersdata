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


class LitreCalculatorForm(forms.Form):
    size_330 = forms.IntegerField(min_value = 0, initial = 0)
    size_500 = forms.IntegerField(min_value = 0, initial = 0)
    size_700 = forms.IntegerField(min_value = 0, initial = 0)
    size_1000 = forms.IntegerField(min_value = 0, initial = 0)
