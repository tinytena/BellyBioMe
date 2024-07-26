from django.urls import path
from . import views

urlpatterns = [
    path("meals/", views.meal_list, name="meal_list"),
    path("meals/create/", views.meal_create, name="meal_create"),
    path("meals/<int:pk>/", views.meal_detail, name="meal_detail"),
    path("meals/<int:pk>/update/", views.meal_update, name="meal_update"),
    path("meals/<int:pk>/delete/", views.meal_delete, name="meal_delete"),
    path("meals/<int:pk>/feedback/", views.feedback_create, name="feedback_create"),
    path(
        "meals/<int:pk>/gut-reaction/",
        views.gut_reaction_create,
        name="gut_reaction_create",
    ),
]
