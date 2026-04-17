from django.urls import path

from .views import (
    HomeView,
    SkillCreateView,
    SkillDeleteView,
    SkillDetailView,
    SkillUpdateView,
    dashboard,
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
    path(
        "skill/<int:pk>/delete/",
        SkillDeleteView.as_view(),
        name="skill_delete",
    ),
]
