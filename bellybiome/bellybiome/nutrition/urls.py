from django.urls import path
from . import views

urlpatterns = [
    path("meals/", views.meal_list, name="meal_list"),
]
