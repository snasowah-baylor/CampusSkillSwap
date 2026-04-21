from django.urls import path

from .views import (
    HomeView,
    SkillCreateView,
    SkillDeleteView,
    SkillDetailView,
    SkillUpdateView,
    UserProfileView,
    add_review,
    dashboard,
    delete_review,
    signup,
)

app_name = "marketplace"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", signup, name="signup"),
    path("dashboard/", dashboard, name="dashboard"),
    path("skill/new/", SkillCreateView.as_view(), name="skill_create"),
    path("skill/<int:pk>/", SkillDetailView.as_view(), name="skill_detail"),
    path("skill/<int:pk>/edit/", SkillUpdateView.as_view(), name="skill_edit"),
    path("skill/<int:pk>/delete/", SkillDeleteView.as_view(), name="skill_delete"),
    path("skill/<int:pk>/review/", add_review, name="add_review"),
    path("review/<int:pk>/delete/", delete_review, name="delete_review"),
    path("user/<str:username>/", UserProfileView.as_view(), name="user_profile"),
]
