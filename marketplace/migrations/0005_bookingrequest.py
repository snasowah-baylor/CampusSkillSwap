from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0004_contact_info"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(
                    choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")],
                    default="pending",
                    max_length=10,
                )),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at",   models.DateTimeField(auto_now=True)),
                ("skill", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="booking_requests",
                    to="marketplace.skill",
                )),
                ("requester", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="booking_requests_sent",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                "ordering": ["-requested_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="bookingrequest",
            constraint=models.UniqueConstraint(fields=["skill", "requester"], name="one_request_per_skill"),
        ),
    ]
