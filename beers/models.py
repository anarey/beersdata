from django.db import models

class Ingredient(models.Model):
    TYPE_INGREDIENT = (
        ('Y','Yeast'),
        ('M','Malt'),
        ('H','hop'),
        ('O','other'),
    )
    name = models.CharField(max_length=100, unique = True)
    type_ingredient = models.CharField(max_length=1, choices = TYPE_INGREDIENT)

class Recipe(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField(default=0)

class Beer(models.Model):
    beer_name = models.CharField(max_length=50)
    beer_code = models.CharField(max_length=4)
    brewing_date = models.DateTimeField('Date brewing')
    bottle_date = models.DateTimeField('Date bottled')
    alcohol = models.IntegerField(default=0)
    ibu = models.IntegerField(default=0)
    recipe = models.ManyToManyField(Recipe)
