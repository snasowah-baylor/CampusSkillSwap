from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

User = get_user_model()


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("Academic", "Academic tutoring"),
        ("Creative", "Creative services"),
        ("Technical", "Technical help"),
        ("Lifestyle", "Lifestyle support"),
    ]

    CONTACT_PREFERENCE_CHOICES = [
        ("email", "Email"),
        ("chat", "Chat or DM"),
        ("phone", "Phone"),
        ("in_person", "In person"),
    ]

    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("busy", "Busy"),
        ("unavailable", "Unavailable"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES,
        default="Academic",
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Leave empty if this skill is offered for free.",
    )
    is_free = models.BooleanField(
        default=False,
        help_text="Mark this if the skill is free.",
    )
    contact_preference = models.CharField(
        max_length=25,
        choices=CONTACT_PREFERENCE_CHOICES,
        default="email",
    )
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )
    active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide the post from the public listing.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def display_price(self):
        if self.is_free:
            return "Free"
        if self.price is None:
            return "Contact for price"
        return f"${self.price:.2f}"

    def average_rating(self):
        result = self.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(result, 1) if result else None

    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    skill    = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="reviews_given")
    rating   = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
    )
    comment  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["skill", "reviewer"],
                name="one_review_per_skill",
            )
        ]

    def __str__(self):
        return f"{self.reviewer.username} → {self.skill.title} ({self.rating}★)"

    @property
    def star_range(self):
        return range(1, 6)
