# Generated by Django 5.1.7 on 2025-04-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
    ]
