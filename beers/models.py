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
    def __str__(self):
        return self.name + " [" + self.type_ingredient + "]"

class Beer(models.Model):
    beer_name = models.CharField(max_length=50)
    beer_code = models.CharField(max_length=4)
    brewing_date = models.DateField('Date brewing')
    bottle_date = models.DateField('Date bottled', blank = True, null = True)
    alcohol = models.FloatField(default=0, blank = True, null = True)
    ibu = models.FloatField(default=0, blank = True, null = True)

    def __str__(self):
        return self.beer_name

class Recipe(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField(default = 0)
    beer = models.ForeignKey(Beer, default = '-1')

    def __str__(self):
        return (self.ingredient.name + ": " + str(self.quantity)) + " gr"

    def more_info(self):
        return ("[" +self.beer.beer_name + "] " + self.ingredient.name + ": " + str(self.quantity)) + " gr"

class Purchase(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField(default = 0)
    buying_date = models.DateField('Date buying')
    sell_by_date = models.DateField('Date sell-by')
    finished = models.BooleanField(default = False)

    def __str__(self):
        return (self.ingredient.name + ": " + str(self.quantity)) + " gr"
