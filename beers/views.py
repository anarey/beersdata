from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views import generic
from django.shortcuts import render

from .models import Beer, Ingredient, Recipe, Purchase
from .forms import BeerForm, RecipeForm, IngredientForm, PurchaseForm, LitreCalculatorForm

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

    def get_context_data(self, **kwargs):
        context = super(IngredientDetailView, self).get_context_data(**kwargs)
        buying_list = Purchase.objects.filter(ingredient=self.kwargs['pk']).order_by('buying_date')
        context['buying_list'] = buying_list
        return context


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
def ingredient_quantity_exists(ingredient, quantity):
    """ Comprueba si hay existencias de la cantidad 'quantity' del ingrediente 'ingredient'
    para una receta.
    """

    exists = False
    ingredient_total = 0
    list_purchase = Purchase.objects.filter(ingredient = ingredient)
    for purchase in list_purchase:
        if purchase.quantity > purchase.finished:
            ingredient_total = ingredient_total + purchase.existence()

    if ingredient_total >= quantity:
        exists = True

    return exists


def ingredient_quantity_decrement(ingredient, quantity):
    """ Decrementa la cantidad 'quantity' del inventario del ingrediente
    'ingredient' para una receta. Retorna True si no hubo problemas.
    """

    if not ingredient_quantity_exists(ingredient, quantity):
        return False

    list_purchase = Purchase.objects.filter(ingredient = ingredient)
    for purchase in list_purchase:
        if quantity == 0:
            break
        elif purchase.quantity == purchase.finished:
            continue
        elif purchase.existence() >= quantity:
            purchase.finished = purchase.finished + quantity
            quantity = 0
        elif (purchase.existence() < quantity):
            quantity = quantity - purchase.existence()
            purchase.finished = purchase.finished - purchase.existence()
        purchase.save()

    if quantity == 0:
        exists = True

    return False


def recipe_new(request, pk):
    beer = get_object_or_404(Beer, pk=pk)

    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            ## Comprobamos si hay la cantidad ese ingrediente recipe.ingredient en existencias
            exists = ingredient_quantity_exists(recipe.ingredient, recipe.quantity)
            if not exists:
                # No hay ingredientes suficientes.
                form = RecipeForm()
                error = "There is not enough quantity of '" + str(recipe.ingredient.name) + "'"
                return render(request, 'beers/recipe_edit.html', {'form': form, 'beer': beer, 'error': error})
            else:
                ingredient_quantity_decrement(recipe.ingredient, recipe.quantity)

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


def ingredient_edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save()
            return HttpResponseRedirect(reverse('beers:beer_detail',
                                                args=(beer.pk)))
    else:
        form = BeerForm(instance=beer)
    return render(request, 'beers/beer_edit.html', {'form': form})


def ingredient_new(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return HttpResponseRedirect(reverse('beers:ingredient_detail',
                                                args=(ingredient.pk,)))
    else:
        form = IngredientForm()
    return render(request, 'beers/ingredient_edit.html', {'form': form})


def ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save()
            return HttpResponseRedirect(reverse('beers:ingredient_detail',
                                                args=(ingredient.pk,)))
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'beers/ingredient_edit.html', {'form': form})

## Compras:
class PurchaseDetailView(generic.DetailView):
    model = Purchase
    template_name = 'beers/purchase_detail.html'

class PurchaseIndexView(generic.ListView):
    template_name = 'beers/purchase_index.html'
    context_object_name = 'purchase_list'

    def get_queryset(self):
        """Return all Purchase."""
        return Purchase.objects.order_by('buying_date').order_by('-ingredient')

def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=beer)
        if form.is_valid():
            purchase = form.save()
            return HttpResponseRedirect(reverse('beers:purchase_detail',
                                                args=(purchase.pk)))
    else:
        form = PurchaseForm(instance=beer)
    return render(request, 'beers/purchase_edit.html', {'form': form})


def purchase_new(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            return HttpResponseRedirect(reverse('beers:purchase_detail',
                                                args=(purchase.pk,)))
    else:
        form = PurchaseForm()
    return render(request, 'beers/purchase_edit.html', {'form': form})


def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            purchase = form.save(commit=false)
            return HttpResponseRedirect(reverse('beers:purchase_detail',
                                                args=(purchase.pk,)))
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'beers/purchase_edit.html', {'form': form})


def litre_calculator(request):
    if request.method == "POST":
        form = LitreCalculatorForm(request.POST)
        if form.is_valid():
            size_330 = form.cleaned_data['size_330']
            size_500 = form.cleaned_data['size_500']
            size_700 = form.cleaned_data['size_700']
            size_1000 = form.cleaned_data['size_1000']
            litre = (0.330 * size_330 + 0.5 * size_500 + 0.7 * size_700 + \
                1 * size_1000)
        return render(request, 'beers/calculator.html', {'form': form,
                                                         'litre': litre})

    else:
        form = LitreCalculatorForm()
    return render(request, 'beers/calculator.html', {'form': form})


def ingredient_stock(request):
    stock = {}
    no_stock = {}
    list_ingredient = Ingredient.objects.all()
    for ingredient in list_ingredient:
        list_purchase = Purchase.objects.filter(ingredient = ingredient)
        ingredient_stock = 0
        for purchase in list_purchase:
            ingredient_stock = ingredient_stock + purchase.existence()
        if ingredient_stock > 0:
            stock[ingredient] = ingredient_stock
        else:
            no_stock[ingredient] = 0
    return render(request,   'beers/ingredient_stock.html',
                  {'stock':stock, 'no_stock':no_stock })
