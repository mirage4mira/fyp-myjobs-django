# Generated by Django 5.1.7 on 2025-04-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0007_create_job_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
