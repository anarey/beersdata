from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail-beers'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.beer_edit, name='beer_edit'),

    url(r'^ingredient/$', views.IndexViewIngredient.as_view(), name='index-ingredients'),
    url(r'^ingredient/(?P<pk>[0-9]+)/$', views.DetailViewIngredient.as_view(), name='detail-ingredients'),
    url(r'^new/$', views.beer_new, name='beer_new'),
]
