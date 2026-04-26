from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BookingRequestForm, ReviewForm, SkillForm, SignupForm
from .models import BookingRequest, Review, Skill

User = get_user_model()

SORT_OPTIONS = [
    ("-created_at", "Newest first"),
    ("created_at", "Oldest first"),
    ("-avg_rating", "Highest rated"),
    ("price", "Price: low to high"),
    ("-price", "Price: high to low"),
]


class HomeView(ListView):
    model = Skill
    template_name = "marketplace/home.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self):
        queryset = Skill.objects.filter(active=True).annotate(avg_rating=Avg("reviews__rating"))

        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "")
        availability = self.request.GET.get("availability", "")
        contact = self.request.GET.get("contact", "")
        price_filter = self.request.GET.get("price", "")
        sort = self.request.GET.get("sort", "-created_at")

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

        valid_sorts = {s[0] for s in SORT_OPTIONS}
        if sort not in valid_sorts:
            sort = "-created_at"

        # Push nulls to end for rating sort
        if sort == "-avg_rating":
            from django.db.models import F
            queryset = queryset.order_by(F("avg_rating").desc(nulls_last=True))
        else:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get = self.request.GET
        context.update({
            "query": get.get("q", ""),
            "selected_category": get.get("category", ""),
            "selected_availability": get.get("availability", ""),
            "selected_contact": get.get("contact", ""),
            "selected_price": get.get("price", ""),
            "selected_sort": get.get("sort", "-created_at"),
            "categories": Skill.CATEGORY_CHOICES,
            "availabilities": Skill.AVAILABILITY_CHOICES,
            "contacts": Skill.CONTACT_PREFERENCE_CHOICES,
            "sort_options": SORT_OPTIONS,
        })
        return context


class SkillDetailView(DetailView):
    model = Skill
    template_name = "marketplace/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.object
        reviews = skill.reviews.select_related("reviewer").all()
        user = self.request.user
        user_review = reviews.filter(reviewer=user).first() if user.is_authenticated else None

        more_from_owner = (
            Skill.objects.filter(owner=skill.owner, active=True)
            .exclude(pk=skill.pk)
            .annotate(avg_rating=Avg("reviews__rating"))[:4]
        )

        user_booking = (
            BookingRequest.objects.filter(skill=skill, requester=user).first()
            if user.is_authenticated else None
        )

        context.update({
            "reviews": reviews,
            "review_count": reviews.count(),
            "average_rating": skill.average_rating(),
            "review_form": ReviewForm(),
            "user_review": user_review,
            "can_review": (
                user.is_authenticated
                and skill.owner != user
                and user_review is None
            ),
            "more_from_owner": more_from_owner,
            "user_booking": user_booking,
            "can_request": (
                user.is_authenticated
                and skill.owner != user
                and user_booking is None
            ),
            "booking_form": BookingRequestForm(),
        })
        return context


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "marketplace/post_form.html"
    success_url = reverse_lazy("marketplace:dashboard")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Your skill post was created successfully.")
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = "marketplace/post_form.html"
    success_url = reverse_lazy("marketplace:dashboard")

    def get_queryset(self):
        return Skill.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your skill post was updated successfully.")
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


class UserProfileView(DetailView):
    model = User
    template_name = "marketplace/user_profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        skills = (
            Skill.objects.filter(owner=profile_user, active=True)
            .annotate(avg_rating=Avg("reviews__rating"))
        )
        agg = Review.objects.filter(skill__owner=profile_user).aggregate(
            total=Count("id"), avg=Avg("rating")
        )
        context.update({
            "skills": skills,
            "skill_count": skills.count(),
            "review_total": agg["total"] or 0,
            "avg_rating": round(agg["avg"], 1) if agg["avg"] else None,
        })
        return context


@login_required
def dashboard(request):
    posts = request.user.skills.all().annotate(avg_rating=Avg("reviews__rating"))
    agg = Review.objects.filter(skill__owner=request.user).aggregate(
        total=Count("id"), avg=Avg("rating")
    )
    pending_requests = BookingRequest.objects.filter(
        skill__owner=request.user, status="pending"
    ).count()
    return render(request, "marketplace/dashboard.html", {
        "posts": posts,
        "active_count": posts.filter(active=True).count(),
        "review_total": agg["total"] or 0,
        "avg_rating": round(agg["avg"], 1) if agg["avg"] else None,
        "pending_requests": pending_requests,
    })


@login_required
def add_review(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if skill.owner == request.user:
        messages.error(request, "You cannot review your own skill.")
        return redirect("marketplace:skill_detail", pk=pk)
    if Review.objects.filter(skill=skill, reviewer=request.user).exists():
        messages.error(request, "You have already reviewed this skill.")
        return redirect("marketplace:skill_detail", pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.skill = skill
            review.reviewer = request.user
            review.save()
            messages.success(request, "Your review was submitted. Thank you!")
        else:
            messages.error(request, "Please correct the errors in your review.")
    return redirect("marketplace:skill_detail", pk=pk)


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, reviewer=request.user)
    skill_pk = review.skill.pk
    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review was deleted.")
    return redirect("marketplace:skill_detail", pk=skill_pk)


@login_required
def request_booking(request, pk):
    skill = get_object_or_404(Skill, pk=pk, active=True)
    if skill.owner == request.user:
        messages.error(request, "You cannot request your own skill.")
        return redirect("marketplace:skill_detail", pk=pk)
    if BookingRequest.objects.filter(skill=skill, requester=request.user).exists():
        messages.error(request, "You have already sent a request for this skill.")
        return redirect("marketplace:skill_detail", pk=pk)
    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.skill = skill
            booking.requester = request.user
            booking.save()
            messages.success(request, "Your session request was sent!")
    return redirect("marketplace:skill_detail", pk=pk)


@login_required
def my_requests(request):
    sent = BookingRequest.objects.filter(
        requester=request.user
    ).select_related("skill", "skill__owner")
    received = BookingRequest.objects.filter(
        skill__owner=request.user
    ).select_related("skill", "requester")
    return render(request, "marketplace/requests.html", {
        "sent": sent,
        "received": received,
    })


@login_required
def respond_to_request(request, pk):
    booking = get_object_or_404(BookingRequest, pk=pk, skill__owner=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            booking.status = "accepted"
            booking.save()
            messages.success(request, f"You accepted {booking.requester.username}'s request.")
        elif action == "decline":
            booking.status = "declined"
            booking.save()
            messages.info(request, f"You declined {booking.requester.username}'s request.")
    return redirect("marketplace:my_requests")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("marketplace:home")
        messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, "marketplace/signup.html", {"form": form})
