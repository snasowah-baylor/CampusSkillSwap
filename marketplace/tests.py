"""
Campus SkillSwap — Test Suite
Covers models, forms, views, and the booking system end-to-end.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import BookingRequest, Review, Skill

User = get_user_model()


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_user(username="alice", password="testpass123"):
    return User.objects.create_user(username=username, password=password)


def make_skill(owner, **kwargs):
    defaults = dict(
        title="Python Tutoring",
        description="I can help you learn Python.",
        category="Technical",
        is_free=True,
        contact_preference="email",
        availability_status="available",
        active=True,
    )
    defaults.update(kwargs)
    return Skill.objects.create(owner=owner, **defaults)


def make_review(skill, reviewer, rating=4, comment="Great!"):
    return Review.objects.create(
        skill=skill, reviewer=reviewer, rating=rating, comment=comment
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODEL UNIT TESTS
# ══════════════════════════════════════════════════════════════════════════════

class SkillModelTest(TestCase):
    def setUp(self):
        self.owner = make_user("owner")
        self.skill = make_skill(self.owner)

    def test_str(self):
        self.assertEqual(str(self.skill), "Python Tutoring")

    def test_display_price_free(self):
        self.assertEqual(self.skill.display_price(), "Free")

    def test_display_price_with_amount(self):
        self.skill.is_free = False
        self.skill.price = 25.00
        self.skill.save()
        self.assertEqual(self.skill.display_price(), "$25.00")

    def test_display_price_contact(self):
        self.skill.is_free = False
        self.skill.price = None
        self.skill.save()
        self.assertEqual(self.skill.display_price(), "Contact for price")

    def test_average_rating_no_reviews(self):
        self.assertIsNone(self.skill.average_rating())

    def test_average_rating_with_reviews(self):
        reviewer = make_user("reviewer")
        make_review(self.skill, reviewer, rating=4)
        self.assertEqual(self.skill.average_rating(), 4.0)

    def test_review_count(self):
        reviewer = make_user("reviewer")
        make_review(self.skill, reviewer, rating=5)
        self.assertEqual(self.skill.review_count(), 1)

    def test_review_count_zero(self):
        self.assertEqual(self.skill.review_count(), 0)

    def test_default_ordering_newest_first(self):
        skill2 = make_skill(self.owner, title="Skill B")
        skills = list(Skill.objects.all())
        self.assertEqual(skills[0], skill2)

    def test_active_default_true(self):
        self.assertTrue(self.skill.active)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.owner    = make_user("owner")
        self.reviewer = make_user("reviewer")
        self.skill    = make_skill(self.owner)
        self.review   = make_review(self.skill, self.reviewer, rating=3)

    def test_str(self):
        self.assertIn("reviewer", str(self.review))
        self.assertIn("Python Tutoring", str(self.review))
        self.assertIn("3", str(self.review))

    def test_star_range(self):
        self.assertEqual(list(self.review.star_range), [1, 2, 3, 4, 5])

    def test_unique_constraint(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                skill=self.skill, reviewer=self.reviewer, rating=5
            )

    def test_rating_stored_correctly(self):
        self.assertEqual(self.review.rating, 3)


class BookingRequestModelTest(TestCase):
    def setUp(self):
        self.owner     = make_user("owner")
        self.requester = make_user("requester")
        self.skill     = make_skill(self.owner)
        self.booking   = BookingRequest.objects.create(
            skill=self.skill, requester=self.requester, message="Hi!"
        )

    def test_str(self):
        self.assertIn("requester", str(self.booking))
        self.assertIn("Python Tutoring", str(self.booking))
        self.assertIn("pending", str(self.booking))

    def test_default_status_pending(self):
        self.assertEqual(self.booking.status, "pending")

    def test_unique_constraint(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            BookingRequest.objects.create(
                skill=self.skill, requester=self.requester
            )

    def test_status_choices(self):
        self.booking.status = "accepted"
        self.booking.save()
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "accepted")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW INTEGRATION TESTS
# ══════════════════════════════════════════════════════════════════════════════

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner  = make_user("alice")
        self.skill1 = make_skill(self.owner, title="Python Tutoring", category="Technical")
        self.skill2 = make_skill(self.owner, title="Guitar Lessons", category="Creative")
        self.skill3 = make_skill(self.owner, title="Yoga Class", category="Lifestyle", active=False)

    def test_home_loads(self):
        r = self.client.get(reverse("marketplace:home"))
        self.assertEqual(r.status_code, 200)

    def test_home_shows_active_skills_only(self):
        r = self.client.get(reverse("marketplace:home"))
        titles = [p.title for p in r.context["posts"]]
        self.assertIn("Python Tutoring", titles)
        self.assertIn("Guitar Lessons", titles)
        self.assertNotIn("Yoga Class", titles)

    def test_search_by_title(self):
        r = self.client.get(reverse("marketplace:home") + "?q=guitar")
        titles = [p.title for p in r.context["posts"]]
        self.assertIn("Guitar Lessons", titles)
        self.assertNotIn("Python Tutoring", titles)

    def test_filter_by_category(self):
        r = self.client.get(reverse("marketplace:home") + "?category=Technical")
        titles = [p.title for p in r.context["posts"]]
        self.assertIn("Python Tutoring", titles)
        self.assertNotIn("Guitar Lessons", titles)

    def test_filter_free(self):
        make_skill(self.owner, title="Paid Skill", is_free=False, price=10)
        r = self.client.get(reverse("marketplace:home") + "?price=free")
        for post in r.context["posts"]:
            self.assertTrue(post.is_free)

    def test_filter_paid(self):
        make_skill(self.owner, title="Paid Skill", is_free=False, price=10)
        r = self.client.get(reverse("marketplace:home") + "?price=paid")
        for post in r.context["posts"]:
            self.assertFalse(post.is_free)

    def test_sort_context_passed(self):
        r = self.client.get(reverse("marketplace:home") + "?sort=-created_at")
        self.assertEqual(r.context["selected_sort"], "-created_at")

    def test_empty_search_shows_no_results(self):
        r = self.client.get(reverse("marketplace:home") + "?q=zzznomatch")
        self.assertEqual(len(r.context["posts"]), 0)


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_page_loads(self):
        r = self.client.get(reverse("marketplace:signup"))
        self.assertEqual(r.status_code, 200)

    def test_signup_creates_user_and_redirects(self):
        r = self.client.post(reverse("marketplace:signup"), {
            "username": "newuser",
            "password1": "complexpass99!",
            "password2": "complexpass99!",
            "email": "new@example.com",
        })
        self.assertRedirects(r, reverse("marketplace:home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_invalid_password_mismatch(self):
        r = self.client.post(reverse("marketplace:signup"), {
            "username": "newuser",
            "password1": "complexpass99!",
            "password2": "wrongpassword",
        })
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = make_user("alice")
        self.skill  = make_skill(self.user)

    def test_dashboard_redirects_anonymous(self):
        r = self.client.get(reverse("marketplace:dashboard"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_dashboard_loads_for_authenticated(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.get(reverse("marketplace:dashboard"))
        self.assertEqual(r.status_code, 200)

    def test_dashboard_shows_own_skills(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.get(reverse("marketplace:dashboard"))
        titles = [p.title for p in r.context["posts"]]
        self.assertIn("Python Tutoring", titles)

    def test_dashboard_stat_active_count(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.get(reverse("marketplace:dashboard"))
        self.assertEqual(r.context["active_count"], 1)

    def test_dashboard_shows_pending_requests(self):
        requester = make_user("bob")
        BookingRequest.objects.create(skill=self.skill, requester=requester, message="Hi")
        self.client.login(username="alice", password="testpass123")
        r = self.client.get(reverse("marketplace:dashboard"))
        self.assertEqual(r.context["pending_requests"], 1)


class SkillCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice  = make_user("alice")
        self.bob    = make_user("bob")
        self.skill  = make_skill(self.alice)

    def test_create_skill_requires_login(self):
        r = self.client.get(reverse("marketplace:skill_create"))
        self.assertEqual(r.status_code, 302)

    def test_create_skill_post(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.post(reverse("marketplace:skill_create"), {
            "title": "New Skill",
            "description": "Description here.",
            "category": "Academic",
            "is_free": True,
            "contact_preference": "email",
            "availability_status": "available",
            "active": True,
        })
        self.assertRedirects(r, reverse("marketplace:dashboard"))
        self.assertTrue(Skill.objects.filter(title="New Skill", owner=self.alice).exists())

    def test_edit_skill_by_owner(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.post(
            reverse("marketplace:skill_edit", args=[self.skill.pk]),
            {
                "title": "Updated Title",
                "description": "Updated description.",
                "category": "Technical",
                "is_free": True,
                "contact_preference": "email",
                "availability_status": "available",
                "active": True,
            }
        )
        self.assertRedirects(r, reverse("marketplace:dashboard"))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Updated Title")

    def test_edit_skill_blocked_for_non_owner(self):
        self.client.login(username="bob", password="testpass123")
        r = self.client.post(
            reverse("marketplace:skill_edit", args=[self.skill.pk]),
            {"title": "Hacked", "description": "x", "category": "Technical",
             "is_free": True, "contact_preference": "email",
             "availability_status": "available", "active": True}
        )
        self.assertEqual(r.status_code, 404)
        self.skill.refresh_from_db()
        self.assertNotEqual(self.skill.title, "Hacked")

    def test_delete_skill_by_owner(self):
        self.client.login(username="alice", password="testpass123")
        r = self.client.post(reverse("marketplace:skill_delete", args=[self.skill.pk]))
        self.assertRedirects(r, reverse("marketplace:dashboard"))
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_delete_skill_blocked_for_non_owner(self):
        self.client.login(username="bob", password="testpass123")
        r = self.client.post(reverse("marketplace:skill_delete", args=[self.skill.pk]))
        self.assertEqual(r.status_code, 404)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())


class SkillDetailViewTest(TestCase):
    def setUp(self):
        self.client   = Client()
        self.owner    = make_user("owner")
        self.visitor  = make_user("visitor")
        self.skill    = make_skill(self.owner)

    def test_detail_page_loads(self):
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertEqual(r.status_code, 200)

    def test_detail_shows_title(self):
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertContains(r, "Python Tutoring")

    def test_can_review_false_for_owner(self):
        self.client.login(username="owner", password="testpass123")
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertFalse(r.context["can_review"])

    def test_can_review_true_for_other_user(self):
        self.client.login(username="visitor", password="testpass123")
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertTrue(r.context["can_review"])

    def test_can_request_false_for_owner(self):
        self.client.login(username="owner", password="testpass123")
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertFalse(r.context["can_request"])

    def test_can_request_true_for_other_user(self):
        self.client.login(username="visitor", password="testpass123")
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertTrue(r.context["can_request"])

    def test_can_request_false_after_sent(self):
        BookingRequest.objects.create(skill=self.skill, requester=self.visitor)
        self.client.login(username="visitor", password="testpass123")
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertFalse(r.context["can_request"])
        self.assertIsNotNone(r.context["user_booking"])

    def test_average_rating_in_context(self):
        make_review(self.skill, self.visitor, rating=5)
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertEqual(r.context["average_rating"], 5.0)

    def test_review_count_in_context(self):
        make_review(self.skill, self.visitor, rating=3)
        r = self.client.get(reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertEqual(r.context["review_count"], 1)


class ReviewViewTest(TestCase):
    def setUp(self):
        self.client   = Client()
        self.owner    = make_user("owner")
        self.reviewer = make_user("reviewer")
        self.skill    = make_skill(self.owner)

    def test_submit_review(self):
        self.client.login(username="reviewer", password="testpass123")
        r = self.client.post(
            reverse("marketplace:add_review", args=[self.skill.pk]),
            {"rating": 4, "comment": "Very helpful!"}
        )
        self.assertRedirects(r, reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertTrue(Review.objects.filter(skill=self.skill, reviewer=self.reviewer).exists())

    def test_owner_cannot_review_own_skill(self):
        self.client.login(username="owner", password="testpass123")
        self.client.post(
            reverse("marketplace:add_review", args=[self.skill.pk]),
            {"rating": 5, "comment": "Self review"}
        )
        self.assertFalse(Review.objects.filter(skill=self.skill, reviewer=self.owner).exists())

    def test_duplicate_review_rejected(self):
        make_review(self.skill, self.reviewer, rating=3)
        self.client.login(username="reviewer", password="testpass123")
        self.client.post(
            reverse("marketplace:add_review", args=[self.skill.pk]),
            {"rating": 5, "comment": "Second attempt"}
        )
        self.assertEqual(Review.objects.filter(skill=self.skill, reviewer=self.reviewer).count(), 1)

    def test_delete_review_by_owner(self):
        review = make_review(self.skill, self.reviewer)
        self.client.login(username="reviewer", password="testpass123")
        r = self.client.post(reverse("marketplace:delete_review", args=[review.pk]))
        self.assertRedirects(r, reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_delete_review_blocked_for_others(self):
        review = make_review(self.skill, self.reviewer)
        other = make_user("other")
        self.client.login(username="other", password="testpass123")
        r = self.client.post(reverse("marketplace:delete_review", args=[review.pk]))
        self.assertEqual(r.status_code, 404)
        self.assertTrue(Review.objects.filter(pk=review.pk).exists())

    def test_review_requires_login(self):
        r = self.client.post(
            reverse("marketplace:add_review", args=[self.skill.pk]),
            {"rating": 5, "comment": "Hi"}
        )
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Review.objects.exists())


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice  = make_user("alice")
        self.skill  = make_skill(self.alice)

    def test_profile_page_loads(self):
        r = self.client.get(reverse("marketplace:user_profile", args=["alice"]))
        self.assertEqual(r.status_code, 200)

    def test_profile_shows_username(self):
        r = self.client.get(reverse("marketplace:user_profile", args=["alice"]))
        self.assertContains(r, "alice")

    def test_profile_shows_active_skills(self):
        r = self.client.get(reverse("marketplace:user_profile", args=["alice"]))
        titles = [s.title for s in r.context["skills"]]
        self.assertIn("Python Tutoring", titles)

    def test_profile_hides_inactive_skills(self):
        make_skill(self.alice, title="Hidden", active=False)
        r = self.client.get(reverse("marketplace:user_profile", args=["alice"]))
        titles = [s.title for s in r.context["skills"]]
        self.assertNotIn("Hidden", titles)

    def test_profile_404_unknown_user(self):
        r = self.client.get(reverse("marketplace:user_profile", args=["nobody"]))
        self.assertEqual(r.status_code, 404)

    def test_profile_skill_count(self):
        r = self.client.get(reverse("marketplace:user_profile", args=["alice"]))
        self.assertEqual(r.context["skill_count"], 1)


# ══════════════════════════════════════════════════════════════════════════════
# BOOKING / REQUESTS SYSTEM TESTS
# ══════════════════════════════════════════════════════════════════════════════

class BookingRequestViewTest(TestCase):
    def setUp(self):
        self.client    = Client()
        self.owner     = make_user("owner")
        self.requester = make_user("requester")
        self.skill     = make_skill(self.owner)

    def test_send_request_creates_booking(self):
        self.client.login(username="requester", password="testpass123")
        r = self.client.post(
            reverse("marketplace:request_booking", args=[self.skill.pk]),
            {"message": "Can we meet Tuesday?"}
        )
        self.assertRedirects(r, reverse("marketplace:skill_detail", args=[self.skill.pk]))
        self.assertTrue(
            BookingRequest.objects.filter(skill=self.skill, requester=self.requester).exists()
        )

    def test_send_request_requires_login(self):
        r = self.client.post(
            reverse("marketplace:request_booking", args=[self.skill.pk]),
            {"message": "Hi"}
        )
        self.assertEqual(r.status_code, 302)
        self.assertFalse(BookingRequest.objects.exists())

    def test_owner_cannot_request_own_skill(self):
        self.client.login(username="owner", password="testpass123")
        self.client.post(
            reverse("marketplace:request_booking", args=[self.skill.pk]),
            {"message": "Self request"}
        )
        self.assertFalse(
            BookingRequest.objects.filter(skill=self.skill, requester=self.owner).exists()
        )

    def test_duplicate_request_rejected(self):
        BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        self.client.login(username="requester", password="testpass123")
        self.client.post(
            reverse("marketplace:request_booking", args=[self.skill.pk]),
            {"message": "Second request"}
        )
        self.assertEqual(
            BookingRequest.objects.filter(skill=self.skill, requester=self.requester).count(), 1
        )

    def test_my_requests_shows_sent(self):
        booking = BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        self.client.login(username="requester", password="testpass123")
        r = self.client.get(reverse("marketplace:my_requests"))
        self.assertEqual(r.status_code, 200)
        self.assertIn(booking, r.context["sent"])

    def test_my_requests_shows_received(self):
        booking = BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        self.client.login(username="owner", password="testpass123")
        r = self.client.get(reverse("marketplace:my_requests"))
        self.assertIn(booking, r.context["received"])

    def test_my_requests_requires_login(self):
        r = self.client.get(reverse("marketplace:my_requests"))
        self.assertEqual(r.status_code, 302)

    def test_owner_can_accept_request(self):
        booking = BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        self.client.login(username="owner", password="testpass123")
        r = self.client.post(
            reverse("marketplace:respond_request", args=[booking.pk]),
            {"action": "accept"}
        )
        self.assertRedirects(r, reverse("marketplace:my_requests"))
        booking.refresh_from_db()
        self.assertEqual(booking.status, "accepted")

    def test_owner_can_decline_request(self):
        booking = BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        self.client.login(username="owner", password="testpass123")
        self.client.post(
            reverse("marketplace:respond_request", args=[booking.pk]),
            {"action": "decline"}
        )
        booking.refresh_from_db()
        self.assertEqual(booking.status, "declined")

    def test_non_owner_cannot_respond(self):
        booking = BookingRequest.objects.create(skill=self.skill, requester=self.requester)
        other = make_user("other")
        self.client.login(username="other", password="testpass123")
        r = self.client.post(
            reverse("marketplace:respond_request", args=[booking.pk]),
            {"action": "accept"}
        )
        self.assertEqual(r.status_code, 404)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "pending")

    def test_request_on_inactive_skill_fails(self):
        inactive = make_skill(self.owner, title="Inactive", active=False)
        self.client.login(username="requester", password="testpass123")
        r = self.client.post(
            reverse("marketplace:request_booking", args=[inactive.pk]),
            {"message": "Hi"}
        )
        self.assertEqual(r.status_code, 404)
        self.assertFalse(BookingRequest.objects.filter(skill=inactive).exists())

    def test_message_optional(self):
        self.client.login(username="requester", password="testpass123")
        self.client.post(
            reverse("marketplace:request_booking", args=[self.skill.pk]),
            {"message": ""}
        )
        booking = BookingRequest.objects.filter(skill=self.skill, requester=self.requester).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.message, "")
