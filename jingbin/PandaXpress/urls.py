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
    
    path('inven/', views.show_inven, name = "show"),
    path('inven/create/', views.CreateInven, name="create"),
    path('inven/delete/', views.DeleteInven, name='delete'),
    path('inven/update/', views.update_inven, name = 'update'),
    path('inven/adv/', views.advanced, name = 'adv'),
    path('inven/search/', views.search, name = 'search')

]