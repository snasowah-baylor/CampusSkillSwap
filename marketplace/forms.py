from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import BookingRequest, Review, Skill


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()


class SkillForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            "title",
            "description",
            "category",
            "price",
            "is_free",
            "contact_preference",
            "contact_info",
            "availability_status",
            "active",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Math tutoring or graphic design help",
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": (
                        "Describe what you offer and how other students can benefit."
                    ),
                },
            ),
            "price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Leave empty if free",
                },
            ),
            "contact_info": forms.TextInput(
                attrs={
                    "placeholder": "e.g. your@email.com, 555-123-4567, Discord: user#1234",
                },
            ),
            "category": forms.Select(),
            "contact_preference": forms.Select(),
            "availability_status": forms.Select(),
            "is_free": forms.CheckboxInput(),
            "active": forms.CheckboxInput(),
        }
        labels = {
            "is_free": "Offer this service for free",
            "active": "Show this post publicly",
            "contact_preference": "Best way to contact you",
            "contact_info": "Your contact details",
            "availability_status": "Availability status",
        }
        help_texts = {
            "price": "Enter a price or mark the post as free.",
            "contact_info": "Shown to students who want to reach you. Match this to your preferred contact method above.",
        }


class SignupForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = (*UserCreationForm.Meta.fields, "email")


class LoginForm(BootstrapMixin, AuthenticationForm):
    pass


class BookingRequestForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Tell the provider what you need or when you're available (optional).",
            }),
        }
        labels = {"message": "Message (optional)"}


class ReviewForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)],
            ),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience (optional)"}),
        }
        labels = {
            "rating":  "Your rating",
            "comment": "Comment",
        }
