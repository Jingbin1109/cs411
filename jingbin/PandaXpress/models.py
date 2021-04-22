# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Follow(models.Model):
    member = models.ForeignKey('Membership', models.DO_NOTHING,related_name="Follow_member",blank=True, null=True)
    following = models.ForeignKey('Membership', models.DO_NOTHING,related_name="Follow_following", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Follow'


class Has(models.Model):
    recipe = models.ForeignKey('Recipes', models.DO_NOTHING, blank=True, null=True)
    nutrient = models.ForeignKey('Nutrients', models.DO_NOTHING, blank=True, null=True)
    nutrient_amnt = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Has'


class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Ingredients'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    inventory_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Inventory'


class InventoryIncl(models.Model):
    inventory_incl_id = models.AutoField(primary_key=True)
    inventory_id = models.IntegerField()
    ingredient_id = models.IntegerField()
    ingredient_amount = models.FloatField()
    ingredient_unit = models.CharField(max_length=50)
    ingredient_added_date = models.DateField()
    ingredient_expiry_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'Inventory_incl'


class Membership(models.Model):
    member_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Membership'


class Nutrients(models.Model):
    nutrient_id = models.IntegerField(primary_key=True)
    nutrient_name = models.CharField(max_length=25, blank=True, null=True)
    nutrient_description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Nutrients'


class Owns(models.Model):
    member = models.ForeignKey(Membership, models.DO_NOTHING, blank=True, null=True)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Owns'


class RecipeIncl(models.Model):
    recipe = models.OneToOneField('Recipes', models.DO_NOTHING, primary_key=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Recipe_Incl'
        unique_together = (('recipe', 'ingredient'),)


class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_creator = models.ForeignKey(Membership, models.DO_NOTHING, db_column='recipe_creator')
    recipe_name = models.CharField(max_length=1000, blank=True, null=True)
    recipe_genre = models.CharField(max_length=1000, blank=True, null=True)
    recipe_description = models.CharField(max_length=1000, blank=True, null=True)
    recipe_steps = models.TextField(blank=True, null=True)
    cooking_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Recipes'


class Store(models.Model):
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Membership, models.DO_NOTHING, blank=True, null=True)
    recipe_member_rel = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Store'

