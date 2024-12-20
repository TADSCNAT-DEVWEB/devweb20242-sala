# Generated by Django 5.1.2 on 2024-12-18 20:55

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_authorship_book_authorship_book"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookInstance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uniqueID",
                    models.UUIDField(default=uuid.uuid4, verbose_name="ID Único"),
                ),
                (
                    "dueBack",
                    models.DateField(
                        blank=True, null=True, verbose_name="Data da devolução"
                    ),
                ),
                ("imprint", models.CharField(max_length=100, verbose_name="Edição")),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("M", "Maintenence"),
                            ("O", "On Loan"),
                            ("A", "Available"),
                            ("R", "Reserved"),
                        ],
                        default="M",
                        help_text="Book Availability",
                        max_length=1,
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="bookInstances",
                        to="library.book",
                    ),
                ),
            ],
            options={
                "ordering": ["dueBack"],
            },
        ),
    ]