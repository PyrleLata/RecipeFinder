from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.sign_up),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('recipes', views.recipes),
    path('add-recipe', views.add_recipe),
    path('recipes/<int:recipe_id>', views.recipe_info),
    path('recipes/<int:recipe_id>/edit', views.edit_recipe),
    path('recipes/<int:recipe_id>/update', views.update_recipe),
    path('recipes/<int:recipe_id>/destroy', views.destroy_recipe),
    path('recipes/share', views.share_recipe),
    # path('add-recipe', views.add_recipe),
    # path('meals-list', views.meals_list),
    # path('add-post', views.add_post),
#     path('wall', views.wall),
#     path('edit/<int:post_id>', views.edit_post),
#     path('modify-post', views.modify_post),
#     path('add-comment', views.add_comment),
#     path('add-like/<int:post_id>', views.add_like)
]