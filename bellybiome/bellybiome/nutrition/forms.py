from django import forms
from .models import Meal, Feedback, GutReaction


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "description", "calories", "date", "meal_type"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["energy_level", "sleep_quality", "mood", "bowel_movements"]


class GutReactionForm(forms.ModelForm):
    class Meta:
        model = GutReaction
        fields = ["reaction", "reaction_notes"]
