from django.urls import path
from PandaXpress import views

urlpatterns = [
    path("signin/", views.log_in),
    path("signup/", views.sign_up),
    path("",views.Home),
    path("user/",views.User),
    path("follow_recipes/",views.Follow_recipes),
    path("delete_follow/",views.delete_follow),
    path("delete_store/",views.delete_store),
    path("recipe_ingredients/",views.RecInd),
    path('recipe/', views.ShowRecipe, name='recipe'),
    path('recipe/search/', views.SearchRecipe, name='search'),
    path('recipe/create/', views.CreateRecipe, name='create'),
    path('recipe/update/', views.UpdateRecipe, name='update'),
    path('recipe/delete/', views.DeleteRecipe, name='delete'),
    path('recipe/advance', views.AdvancedSearch, name='advance')



]