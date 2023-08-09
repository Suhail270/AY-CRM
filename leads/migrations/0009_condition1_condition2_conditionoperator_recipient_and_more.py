# Generated by Django 4.1.6 on 2023-08-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0008_task_deadline"),
    ]

    operations = [
        migrations.CreateModel(
            name="Condition1",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Condition2",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ConditionOperator",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Recipient",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="RecordSelection",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="RecordSelectionRange",
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
                ("option", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="KPI",
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
                ("name", models.CharField(max_length=100)),
                ("points_per_record", models.IntegerField(default=1)),
                (
                    "points_valueOfField",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "condition1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.condition1",
                    ),
                ),
                (
                    "condition2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.condition2",
                    ),
                ),
                (
                    "conditionOp",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.conditionoperator",
                    ),
                ),
                (
                    "kpi_lead",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.lead",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.recipient",
                    ),
                ),
                (
                    "record_selection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.recordselection",
                    ),
                ),
                (
                    "record_selection_range",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.recordselectionrange",
                    ),
                ),
            ],
        ),
    ]
