# Generated by Django 5.1.7 on 2025-04-07 05:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0011_userprofile_first_name_userprofile_last_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.CharField(blank=True, choices=[('High School', 'High School'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Doctorate', 'Doctorate')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=15)),
                ('home_location', models.CharField(max_length=255)),
                ('education', models.CharField(blank=True, choices=[('High School', 'High School'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Doctorate', 'Doctorate')], max_length=20, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('ApplicantSkill', models.ManyToManyField(related_name='job_applications', to='myjobs.applicantskill')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='myjobs.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantPastJobExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('date_started', models.DateField()),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('job_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_past_job_experiences', to='myjobs.jobapplication')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantLanguageProficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('proficiency', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Fluent', 'Fluent')], max_length=20)),
                ('job_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_language_proficiencies', to='myjobs.jobapplication')),
            ],
        ),
    ]
