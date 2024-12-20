# Generated by Django 5.1.2 on 2024-12-12 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_author_language"),
    ]

    operations = [
        migrations.CreateModel(
            name="Authorship",
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
                ("role", models.CharField(max_length=100, verbose_name="Papel")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="library.author",
                        verbose_name="Autor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=200)),
                (
                    "summary",
                    models.TextField(
                        help_text="Informe o sumário do Livro",
                        max_length=100,
                        verbose_name="Sumário",
                    ),
                ),
                (
                    "isbn",
                    models.CharField(
                        help_text='Informe o <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>',
                        max_length=13,
                        unique=True,
                        verbose_name="ISBN",
                    ),
                ),
                (
                    "authors",
                    models.ManyToManyField(
                        help_text="Selecione os Autores do Livro",
                        related_name="books",
                        through="library.Authorship",
                        to="library.author",
                    ),
                ),
                (
                    "genres",
                    models.ManyToManyField(
                        help_text="Selecione os Gêneros do Livro",
                        related_name="books",
                        to="library.genre",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="library.language",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="authorship",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="library.book",
                verbose_name="Livro",
            ),
        ),
    ]
