from django.shortcuts import render

from django.views import generic

from .models import Beer, Ingredient

class IndexView(generic.ListView):
    template_name = 'beers/index.html'
    context_object_name = 'beers_list'

    def get_queryset(self):
        """Return the last five published beers."""
        return Beer.objects.order_by('-brewing_date')

class DetailView(generic.DetailView):
    model = Beer
    template_name = 'beers/detail.html'

class DetailViewIngredient(generic.DetailView):
    model = Ingredient
    template_name = 'beers/ingredient-detail.html'

class IndexViewIngredient(generic.ListView):
    template_name = 'beers/index-ingredient.html'
    context_object_name = 'ingredient_list'

    def get_queryset(self):
        """Return all Ingredient."""
        return Ingredient.objects.order_by('-type_ingredient').order_by('name')
