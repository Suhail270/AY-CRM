# Generated by Django 4.1.6 on 2023-08-01 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0004_task_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="organization",
            field=models.CharField(default="Motors", max_length=100),
            preserve_default=False,
        ),
    ]
