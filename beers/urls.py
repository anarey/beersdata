from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BeerIndexView.as_view(), name='beer_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.BeerDetailView.as_view(), name='beer_detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.beer_edit, name='beer_edit'),
    url(r'^(?P<pk>[0-9]+)/recipe/new/$', views.recipe_new, name='recipe_new'),
    url(r'^new/$', views.beer_new, name='beer_new'),

    url(r'^ingredient/$', views.IngredientIndexView.as_view(), name='ingredient_index'),
    url(r'^ingredient/(?P<pk>[0-9]+)/$', views.IngredientDetailView.as_view(), name='ingredient_detail'),
    #url(r'^ingredient/new/$', views.ingredient_new, name='ingredient_new'),
    #url(r'^ingredient/(?P<pk>[0-9]+)/edit/$', views.ingredient_edit, name='ingredient_edit'),

    url(r'^recipe/$', views.RecipeIndexView.as_view(), name='recipe_index'),
    url(r'^recipe/(?P<pk>[0-9]+)/$', views.RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^recipe/(?P<pk>[0-9]+)/edit/$', views.recipe_edit, name='recipe_edit'),
]
