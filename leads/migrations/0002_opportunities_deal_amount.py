# Generated by Django 4.1.6 on 2023-08-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunities',
            name='deal_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
