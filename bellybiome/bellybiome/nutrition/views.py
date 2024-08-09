from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meal
from .forms import MealForm, FeedbackForm, GutReactionForm
import requests
from django.http import JsonResponse


@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user)
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
def scan_barcode(request):
    return render(request, "nutrition/scan_barcode.html")


@login_required
def get_food_by_barcode(request, barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data["product"]
            food_data = {
                "name": product.get("product_name"),
                "calories": product.get("nutriments", {}).get("energy-kcal_100g"),
                "nutrients": {
                    "fat": product.get("nutriments", {}).get("fat_100g"),
                    "saturated_fat": product.get("nutriments", {}).get(
                        "saturated-fat_100g"
                    ),
                    "carbohydrates": product.get("nutriments", {}).get(
                        "carbohydrates_100g"
                    ),
                    "sugars": product.get("nutriments", {}).get("sugars_100g"),
                    "fiber": product.get("nutriments", {}).get("fiber_100g"),
                    "proteins": product.get("nutriments", {}).get("proteins_100g"),
                    "salt": product.get("nutriments", {}).get("salt_100g"),
                },
            }
            return JsonResponse(food_data)
        else:
            return JsonResponse({"error": "Food item not found"}, status=404)
    else:
        return JsonResponse(
            {"error": "API request failed"}, status=response.status_code
        )
