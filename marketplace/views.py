from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import SkillForm, SignupForm
from .models import Skill


class HomeView(ListView):
    model = Skill
    template_name = "marketplace/home.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self):
        # Start with active posts only.
        queryset = Skill.objects.filter(active=True)

        # Search terms and filters come from query parameters.
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "")
        availability = self.request.GET.get("availability", "")
        contact = self.request.GET.get("contact", "")
        price_filter = self.request.GET.get("price", "")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(owner__username__icontains=query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if availability:
            queryset = queryset.filter(availability_status=availability)

        if contact:
            queryset = queryset.filter(contact_preference=contact)

        if price_filter == "free":
            queryset = queryset.filter(is_free=True)
        elif price_filter == "paid":
            queryset = queryset.filter(is_free=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "query": self.request.GET.get("q", ""),
                "selected_category": self.request.GET.get("category", ""),
                "selected_availability": self.request.GET.get(
                    "availability",
                    "",
                ),
                "selected_contact": self.request.GET.get("contact", ""),
                "selected_price": self.request.GET.get("price", ""),
                "categories": Skill.CATEGORY_CHOICES,
                "availabilities": Skill.AVAILABILITY_CHOICES,
                "contacts": Skill.CONTACT_PREFERENCE_CHOICES,
            }
        )
        return context


class SkillDetailView(DetailView):
    model = Skill
    template_name = "marketplace/post_detail.html"


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "marketplace/post_form.html"
    success_url = reverse_lazy("marketplace:dashboard")

    def form_valid(self, form):
        # Set the owner automatically to the signed-in user.
        form.instance.owner = self.request.user
        messages.success(
            self.request,
            "Your skill post was created successfully.",
        )
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = "marketplace/post_form.html"
    success_url = reverse_lazy("marketplace:dashboard")

    def get_queryset(self):
        # Only allow the owner to edit their own posts.
        return Skill.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your skill post was updated successfully.",
        )
        return super().form_valid(form)


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = "marketplace/post_confirm_delete.html"
    success_url = reverse_lazy("marketplace:dashboard")

    def get_queryset(self):
        return Skill.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your skill post was deleted.")
        return super().form_valid(form)


@login_required
def dashboard(request):
    posts = request.user.skills.all()
    return render(request, "marketplace/dashboard.html", {"posts": posts})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Welcome! Your account has been created.",
            )
            return redirect("marketplace:home")
        messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, "marketplace/signup.html", {"form": form})
