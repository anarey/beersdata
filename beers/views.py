from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views import generic
from django.shortcuts import render

from .models import Beer, Ingredient, Recipe
from .forms import BeerForm, RecipeForm

class BeerIndexView(generic.ListView):
    template_name = 'beers/beer_index.html'
    context_object_name = 'beers_list'

    def get_queryset(self):
        """Return the last five published beers."""
        return Beer.objects.order_by('-brewing_date')

class BeerDetailView(generic.DetailView):
    model = Beer
    template_name = 'beers/beer_detail.html'

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'beers/ingredient_detail.html'

class IngredientIndexView(generic.ListView):
    template_name = 'beers/ingredient_index.html'
    context_object_name = 'ingredient_list'

    def get_queryset(self):
        """Return all Ingredient."""
        return Ingredient.objects.order_by('-type_ingredient').order_by('name')

class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'beers/recipe_detail.html'

class RecipeIndexView(generic.ListView):
    template_name = 'beers/recipe_index.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        """Return all Ingredient."""
        return Recipe.objects.order_by('-beer')

def beer_new(request):
    if request.method == "POST":
        form = BeerForm(request.POST)
        if form.is_valid():
            beer = form.save()
            return HttpResponseRedirect(reverse('beers:beer_detail',
                                                args=(beer.pk,)))
    else:
        form = BeerForm()
    return render(request, 'beers/beer_edit.html', {'form': form})

def beer_edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    list_recipe = Recipe.objects.filter(beer=pk)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save()
            return HttpResponseRedirect(reverse('beers:beer_detail',
                                                args=(beer.pk, list_recipe)))
    else:
        form = BeerForm(instance=beer)
    return render(request, 'beers/beer_edit.html', {'form': form,
                                                    'list_recipe': list_recipe})


def recipe_new(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.beer = beer
            recipe.save()
            return HttpResponseRedirect(reverse('beers:recipe_detail',
                                                args=(recipe.pk,)))
    else:
        form = RecipeForm()
    return render(request, 'beers/recipe_edit.html', {'form': form, 'beer': beer})


def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(reverse('beers:recipe_detail',
                                                args=(recipe.pk,)))
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'beers/recipe_edit.html', {'form': form})
