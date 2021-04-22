from django.contrib import admin
from PandaXpress import models

# Register your models here.

# Register your models here.
@admin.register(models.Membership)
class ContentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Follow)
class MemberAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Recipes)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RecipeIncl)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Inventory)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Ingredients)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.InventoryIncl)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Nutrients)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Has)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Owns)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Store)
class MessageAdmin(admin.ModelAdmin):
    pass

