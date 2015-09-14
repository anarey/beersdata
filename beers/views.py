from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_list_or_404, get_object_or_404

from django.views import generic
from django.shortcuts import render

from .models import Beer, Ingredient
from .forms import BeerForm

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

def beer_new(request):
    if request.method == "POST":
        form = BeerForm(request.POST)
        if form.is_valid():
            beer = form.save()
#            beer = form.save(commit=False)
#            beer.author = request.user
#            import ipdb; ipdb.set_trace()
            beer.save()
            return HttpResponseRedirect(reverse('beers:detail-beers',
                                                args=(beer.pk,)))
    else:
        form = BeerForm()
    return render(request, 'beers/beer_edit.html', {'form': form})

def beer_edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save(commit=False)
#            beer.author = request.user
            beer.save()
            return HttpResponseRedirect(reverse('beers:detail-beers',
                                                args=(beer.pk,)))
    else:
        form = BeerForm(instance=beer)
    return render(request, 'beers/beer_edit.html', {'form': form})
