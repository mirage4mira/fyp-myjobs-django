# Generated by Django 5.1.7 on 2025-04-09 13:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0017_jobapplication_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
