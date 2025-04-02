from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Skill name (e.g., "Python", "Django")

    def __str__(self):
        return self.name

class LanguageProficiency(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Fluent', 'Fluent'),
    ]
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=100)  # Language name (e.g., "English", "Spanish")
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)  # Proficiency level

    def __str__(self):
        return f"{self.language} ({self.proficiency})"

class JobExperience(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='job_experiences')
    job_title = models.CharField(max_length=255)  # Job title (e.g., "Software Engineer")
    company_name = models.CharField(max_length=255)  # Company name
    date_started = models.DateField()  # Start date
    date_ended = models.DateField(blank=True, null=True)  # End date (nullable for current jobs)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    home_location = models.CharField(max_length=255)
    preferred_job = models.CharField(max_length=255)
    education = models.TextField()
    skills = models.ManyToManyField(Skill, related_name='users')  # Many-to-Many relationship with skills

    def __str__(self):
        return f"{self.user.username}'s Profile"
