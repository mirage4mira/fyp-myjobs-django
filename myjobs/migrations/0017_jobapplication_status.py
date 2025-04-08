# Generated by Django 5.1.7 on 2025-04-08 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0016_alter_applicantskill_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('contacted', 'Contacted'), ('interviewed', 'Interviewed'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')], default='pending', max_length=15),
        ),
    ]
