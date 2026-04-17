from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Skill

User = get_user_model()

# ── Site branding ──────────────────────────────────────────────────────────────
admin.site.site_header = "Campus SkillSwap"
admin.site.site_title  = "SkillSwap Admin"
admin.site.index_title = "Site Administration"


# ── Bulk actions ───────────────────────────────────────────────────────────────
@admin.action(description="Activate selected skill posts")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description="Deactivate selected skill posts")
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.action(description="Set availability → Available")
def set_available(modeladmin, request, queryset):
    queryset.update(availability_status="available")


@admin.action(description="Set availability → Busy")
def set_busy(modeladmin, request, queryset):
    queryset.update(availability_status="busy")


@admin.action(description="Set availability → Unavailable")
def set_unavailable(modeladmin, request, queryset):
    queryset.update(availability_status="unavailable")


@admin.action(description="Mark selected posts as free")
def mark_free(modeladmin, request, queryset):
    queryset.update(is_free=True, price=None)


# ── Skill inline (used inside User admin) ─────────────────────────────────────
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    fields = ("title", "category", "availability_status", "active", "is_free")
    show_change_link = True
    can_delete = False


# ── User admin ─────────────────────────────────────────────────────────────────
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines       = [SkillInline]
    list_display  = ("username", "email", "first_name", "last_name",
                     "skill_count", "is_staff", "is_active", "date_joined")
    list_filter   = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering      = ("-date_joined",)

    def skill_count(self, obj):
        count = obj.skills.count()
        return format_html(
            '<a href="../skill/?owner__id__exact={}">{} post{}</a>',
            obj.pk, count, "s" if count != 1 else "",
        )
    skill_count.short_description = "Skills"


# ── Skill admin ────────────────────────────────────────────────────────────────
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display   = (
        "title", "owner_link", "category_badge",
        "availability_badge", "price_display",
        "contact_preference", "active", "created_at",
    )
    list_editable  = ("active",)
    list_filter    = ("category", "availability_status", "active",
                      "is_free", "contact_preference")
    search_fields  = ("title", "description", "owner__username", "owner__email")
    date_hierarchy = "created_at"
    ordering       = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    actions        = [make_active, make_inactive,
                      set_available, set_busy, set_unavailable, mark_free]

    fieldsets = (
        ("Post Details", {
            "fields": ("owner", "title", "description", "category"),
        }),
        ("Pricing", {
            "fields": ("price", "is_free"),
        }),
        ("Status & Contact", {
            "fields": ("availability_status", "contact_preference", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # ── Custom display columns ─────────────────────────────────────────────────
    def owner_link(self, obj):
        return format_html(
            '<a href="../user/{}/change/">{}</a>',
            obj.owner.pk, obj.owner.username,
        )
    owner_link.short_description = "Owner"
    owner_link.admin_order_field = "owner__username"

    def category_badge(self, obj):
        colors = {
            "Academic":  ("#dbeafe", "#1d4ed8"),
            "Creative":  ("#ede9fe", "#6d28d9"),
            "Technical": ("#d1fae5", "#065f46"),
            "Lifestyle": ("#fef3c7", "#92400e"),
        }
        bg, fg = colors.get(obj.category, ("#f1f5f9", "#475569"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:999px;font-size:0.78rem;font-weight:600;">{}</span>',
            bg, fg, obj.category,
        )
    category_badge.short_description = "Category"
    category_badge.admin_order_field = "category"

    def availability_badge(self, obj):
        colors = {
            "available":   ("#d1fae5", "#065f46"),
            "busy":        ("#fef3c7", "#92400e"),
            "unavailable": ("#fee2e2", "#991b1b"),
        }
        bg, fg = colors.get(obj.availability_status, ("#f1f5f9", "#475569"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:999px;font-size:0.78rem;font-weight:600;">{}</span>',
            bg, fg, obj.get_availability_status_display(),
        )
    availability_badge.short_description = "Availability"
    availability_badge.admin_order_field = "availability_status"

    def price_display(self, obj):
        return obj.display_price()
    price_display.short_description = "Price"
