from django.shortcuts import render
from .models import Meal


def meal_list(request):
    meals = Meal.objects.filter(user=request.user)
    return render(request, "nutrition/meal_list.html", {"meals": meals})
