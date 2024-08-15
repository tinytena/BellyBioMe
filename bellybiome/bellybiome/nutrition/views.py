from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meal
from .forms import MealForm, FeedbackForm, GutReactionForm
import requests
from django.http import JsonResponse
import environ
import logging

env = environ.Env()

logger = logging.getLogger(__name__)

USDA_FOODATA_API = env("USDA_FOODATA_API")


@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user).order_by("meal_type", "-date")
    return render(request, "nutrition/meal_list.html", {"meals": meals})


@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, "nutrition/meal_detail.html", {"meal": meal})


@login_required
def meal_create(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect("meal_detail", pk=meal.pk)
    else:
        form = MealForm()
    return render(request, "nutrition/meal_form.html", {"form": form})


@login_required
def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect("meal_detail", pk=meal.pk)
    else:
        form = MealForm(instance=meal)
    return render(request, "nutrition/meal_form.html", {"form": form})


@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        meal.delete()
        return redirect("meal_list")
    return render(request, "nutrition/meal_confirm_delete.html", {"meal": meal})


@login_required
def feedback_create(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.meal = meal
            feedback.save()
            return redirect("meal_detail", pk=meal.pk)
    else:
        form = FeedbackForm()
    return render(request, "nutrition/feedback_form.html", {"form": form, "meal": meal})


@login_required
def gut_reaction_create(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        form = GutReactionForm(request.POST)
        if form.is_valid():
            gut_reaction = form.save(commit=False)
            gut_reaction.meal = meal
            gut_reaction.save()
            return redirect("meal_detail", pk=meal.pk)
    else:
        form = GutReactionForm()
    return render(
        request, "nutrition/gut_reaction_form.html", {"form": form, "meal": meal}
    )


@login_required
def get_food_by_sr_legacy_keywords(request, keyword):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": keyword,
        "dataType": ["SR Legacy"],
        "pageSize": 10,
        "api_key": USDA_FOODATA_API,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("foods"):
            results = []
            for food_item in data["foods"]:
                food_data = {
                    "name": food_item.get("description"),
                    "calories": next(
                        (
                            nutrient["value"]
                            for nutrient in food_item["foodNutrients"]
                            if nutrient["nutrientId"] == 1008
                        ),
                        None,
                    ),
                    "nutrients": {
                        "fat": next(
                            (
                                nutrient["value"]
                                for nutrient in food_item["foodNutrients"]
                                if nutrient["nutrientId"] == 204
                            ),
                            None,
                        ),
                        "carbohydrates": next(
                            (
                                nutrient["value"]
                                for nutrient in food_item["foodNutrients"]
                                if nutrient["nutrientId"] == 205
                            ),
                            None,
                        ),
                        "proteins": next(
                            (
                                nutrient["value"]
                                for nutrient in food_item["foodNutrients"]
                                if nutrient["nutrientId"] == 203
                            ),
                            None,
                        ),
                    },
                }
                results.append(food_data)
            return JsonResponse({"results": results})
        else:
            return JsonResponse({"error": "No matching food items found"}, status=404)
    else:
        return JsonResponse(
            {"error": "API request failed"}, status=response.status_code
        )
