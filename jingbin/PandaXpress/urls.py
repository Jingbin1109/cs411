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

    path('invenown/show/', views.OwnInventory),
    path('invenown/show/update/', views.UpdateOwnInven),
    path('invenown/show/delete/', views.DeleteOwnInven),
    path('invenown/create/', views.CreateOwnInven),

    path('inven/', views.show_inven, name = "show"),
    path('inven/create/', views.CreateInven, name="create"),
    path('inven/delete/', views.DeleteInven, name='delete'),
    path('inven/update/', views.update_inven, name = 'update'),
    # path('inven/search/', views.search, name = 'search'),
    path('recipe/show/', views.ShowRecipe, name = 'recipe'),
    path('recipe/', views.OwnRecipe, name = 'recipe'),
    path('recipe/detail/',view.DetailRecipe, name = 'detail'),
    path('recipe/search/', views.SearchRecipe, name = 'search'),
    path('recipe/create/', views.CreateRecipe, name = 'create'),
    path('recipe/update/',views.UpdateRecipe,name = 'update'),
    path('recipe/delete/',views.DeleteRecipe,name = 'delete'),
    path('recipe/advance/',views.AdvancedSearch,name = 'advance'),
    path('recipe/popular/',views.storeprocedure),
]