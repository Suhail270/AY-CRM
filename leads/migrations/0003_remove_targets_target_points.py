# Generated by Django 3.1.4 on 2023-08-19 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_targets_target_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targets',
            name='target_points',
        ),
    ]
