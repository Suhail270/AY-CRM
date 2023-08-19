# Generated by Django 4.1.6 on 2023-07-31 08:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0002_remove_lead_first_name_remove_lead_last_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlertOptions",
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
                ("option", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="CalendarDisplayOptions",
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
            name="RepeatOptions",
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
            name="Task",
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
                ("title", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("all_day", models.BooleanField()),
                ("start_date", models.DateTimeField(default=datetime.datetime.now)),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField()),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("referenceURL", models.CharField(max_length=300)),
                ("referenceNotes", models.CharField(max_length=500)),
                (
                    "alert",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.alertoptions",
                    ),
                ),
                (
                    "invitees",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.userprofile",
                    ),
                ),
                (
                    "repeat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.repeatoptions",
                    ),
                ),
                (
                    "showAs",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.calendardisplayoptions",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TravelTimeOptions",
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
            name="TaskAttendees",
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
                    "attendee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.userprofile",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leads.task",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="task",
            name="travel_time",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="leads.traveltimeoptions",
            ),
        ),
    ]
