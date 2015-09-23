from django.contrib import admin

from .models import Recipe, Ingredient, Beer, Purchase

class RecipeInLine(admin.TabularInline):
    model = Recipe
    extra = 3


class BeerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Beer info:',{'fields':['beer_name']}),
        (None,{'fields':['beer_code']}),
        (None,{'fields':['alcohol']}),
        (None,{'fields':['ibu']}),
        (None,{'fields':['brewing_date']}),
        (None,{'fields':['bottle_date']}),

   ]
    list_display = ('beer_name', 'beer_code', 'alcohol', 'ibu')
    list_filter = ['brewing_date','alcohol' ]
    ordering = ['brewing_date']

    inlines = [RecipeInLine]

class IngredientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields':['name']}),
        ('Ingredient type',{'fields':['type_ingredient']}),

    ]
    list_filter = ['type_ingredient' ]
    list_display = ('name', 'type_ingredient')

class PurchaseAdmin(admin.ModelAdmin):
    list_filter = ['ingredient' ]

admin.site.register(Beer, BeerAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Purchase, PurchaseAdmin)
