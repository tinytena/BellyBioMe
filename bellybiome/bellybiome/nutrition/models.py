from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    calories = models.PositiveIntegerField()
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def clean(self):
        if self.calories < 0:
            raise ValidationError("Calories cannot be negative.")

    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        ordering = ["-date"]


class Feedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    meal = models.OneToOneField(Meal, on_delete=models.CASCADE)
    energy_level = models.IntegerField(choices=RATING_CHOICES)
    sleep_quality = models.IntegerField(choices=RATING_CHOICES)
    mood = models.IntegerField(choices=RATING_CHOICES)
    bowel_movements = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.meal.name}"

    def clean(self):
        if self.energy_level < 1 or self.energy_level > 5:
            raise ValidationError("Energy level must be between 1 and 5.")
        if self.sleep_quality < 1 or self.sleep_quality > 5:
            raise ValidationError("Sleep quality must be between 1 and 5.")
        if self.mood < 1 or self.mood > 5:
            raise ValidationError("Mood must be between 1 and 5.")
        if self.bowel_movements < 0 or self.bowel_movements > 10:
            raise ValidationError("Bowel movements must be between 0 and 10.")

    class Meta:
        ordering = ["-timestamp"]


class GutReaction(models.Model):
    REACTION_CHOICES = [
        (1, "😞"),  # Very unhappy
        (2, "🙁"),  # Unhappy
        (3, "😐"),  # Neutral
        (4, "🙂"),  # Happy
        (5, "😄"),  # Very happy
    ]

    meal = models.OneToOneField(Meal, on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=REACTION_CHOICES)
    reaction_notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Gut reaction for {self.meal.name}: {self.get_reaction_display()}"

    class Meta:
        ordering = ["-timestamp"]
