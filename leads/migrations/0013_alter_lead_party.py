# Generated by Django 4.1.6 on 2023-08-14 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0012_alter_lead_party'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.parties'),
        ),
    ]
