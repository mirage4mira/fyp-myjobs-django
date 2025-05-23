from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now  # Import for auto date field
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, date

class Skill(models.Model):
    SKILL_CHOICES = [
        ('Programming', 'Programming'),
        ('Data Analysis', 'Data Analysis'),
        ('Project Management', 'Project Management'),
        ('Graphic Design', 'Graphic Design'),
        ('Digital Marketing', 'Digital Marketing'),
        ('Sales', 'Sales'),
        ('Customer Service', 'Customer Service'),
        ('Content Writing', 'Content Writing'),
        ('Public Speaking', 'Public Speaking'),
        ('Problem Solving', 'Problem Solving'),
    ]
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='skills',null=True)
    name = models.CharField(max_length=100, choices=SKILL_CHOICES)  # Limited to predefined choices

    def __str__(self):
        return self.name

class LanguageProficiency(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Fluent', 'Fluent'),
    ]
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Mandarin', 'Mandarin'),
        ('Malay', 'Malay'),
        ('Tamil', 'Tamil'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('German', 'German'),
        ('Japanese', 'Japanese'),
        ('Korean', 'Korean'),
        ('Arabic', 'Arabic'),
    ]
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)  # Limited to predefined choices
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

class PreferredJobClassification(models.Model):
    JOB_CLASSIFICATION_CHOICES = [
        ('Engineering', 'Engineering'),
        ('Data & Analytics', 'Data & Analytics'),
        ('Product Management', 'Product Management'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Human Resources', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Customer Support', 'Customer Support'),
    ]
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='preferred_jobs')
    job_classification = models.CharField(max_length=255, choices=JOB_CLASSIFICATION_CHOICES)  # Limited to predefined choices

    def __str__(self):
        return f"{self.job_classification}"

class UserProfile(models.Model):
    class EducationChoices(models.TextChoices):
        HIGH_SCHOOL = 'High School', 'High School'
        BACHELORS = 'Bachelors', 'Bachelors'
        MASTERS = 'Masters', 'Masters'
        DOCTORATE = 'Doctorate', 'Doctorate'

    HOME_LOCATION_CHOICES = [
        ('Kuala Lumpur', 'Kuala Lumpur'),
        ('George Town', 'George Town'),
        ('Ipoh', 'Ipoh'),
        ('Shah Alam', 'Shah Alam'),
        ('Petaling Jaya', 'Petaling Jaya'),
        ('Johor Bahru', 'Johor Bahru'),
        ('Malacca City', 'Malacca City'),
        ('Alor Setar', 'Alor Setar'),
        ('Kota Bharu', 'Kota Bharu'),
        ('Kuala Terengganu', 'Kuala Terengganu'),
        ('Kuantan', 'Kuantan'),
        ('Seremban', 'Seremban'),
        ('Kuching', 'Kuching'),
        ('Miri', 'Miri'),
        ('Kota Kinabalu', 'Kota Kinabalu'),
        ('Sandakan', 'Sandakan'),
        ('Tawau', 'Tawau'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True, blank=True)  # New first name field
    last_name = models.CharField(max_length=30, null=True, blank=True)  # New last name field
    home_location = models.CharField(max_length=255, choices=HOME_LOCATION_CHOICES)  # Limited to predefined choices
    education = models.CharField(
        max_length=20,
        choices=EducationChoices.choices,
        null=True,
        blank=True
    )  # Updated to use enum choices
    bio = models.TextField(null=True)  # New field
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # New phone number field

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile', default=None)  # Link to User with default
    company_name = models.CharField(max_length=255)  # Name of the company
    company_address = models.TextField()  # Address of the company
    phone_number = models.CharField(max_length=15)  # Contact phone number
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # Company logo
    company_bio = models.TextField(blank=True, null=True)  # Short bio or description of the company

    def __str__(self):
        return self.company_name

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, choices=UserProfile.HOME_LOCATION_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_candidates = models.PositiveIntegerField()
    required_education = models.CharField(
        max_length=20,
        choices=UserProfile.EducationChoices.choices,
        null=True,
        blank=True
    )
    required_experience_years = models.PositiveIntegerField()
    company = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')  # Link to Employer
    job_type = models.CharField(
        max_length=10,
        choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time')],
        default='full_time'
    )
    date_created_or_renewed = models.DateField(default=now)  # Updated field to represent creation or renewal date
    job_category = models.CharField(
        max_length=255,
        choices=PreferredJobClassification.JOB_CLASSIFICATION_CHOICES,
        null=True,
        blank=True
    )  # Job category based on predefined choices

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')  # Link to User
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')  # Link to Job
    first_name = models.CharField(max_length=30)  # Applicant's first name
    last_name = models.CharField(max_length=30)  # Applicant's last name
    phone_number = models.CharField(max_length=15)  # Applicant's phone number
    home_location = models.CharField(max_length=255)  # Applicant's home location
    education = models.CharField(
        max_length=20,
        choices=UserProfile.EducationChoices.choices,
        null=True,
        blank=True
    )  # Applicant's education level
    status = models.CharField(
        max_length=15,
        choices=[
            ('pending', 'Pending'),
            ('contacted', 'Contacted'),
            ('interviewed', 'Interviewed'),
            ('confirmed', 'Confirmed'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )  # Application status
    bio = models.TextField(null=True, blank=True)  # Applicant's bio
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Resume upload
    email = models.EmailField(max_length=255,null=True)  # Applicant's email address
   
    def __str__(self):
        return f"Application by {self.user.username} for {self.job.title}"

class ApplicantSkill(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicant_skills',null=True)  # Link to JobApplication
    name = models.CharField(max_length=100, choices=Skill.SKILL_CHOICES)  # Limited to predefined choices
    def __str__(self):
        return f"{self.skill.name} for {self.job_application}"

class ApplicantLanguageProficiency(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicant_language_proficiencies')  # Link to JobApplication
    language = models.CharField(max_length=100, choices=LanguageProficiency.LANGUAGE_CHOICES)  # Language name
    proficiency = models.CharField(
        max_length=20,
        choices=LanguageProficiency.PROFICIENCY_CHOICES
    )  # Proficiency level

    def __str__(self):
        return f"{self.language} ({self.proficiency}) for {self.job_application}"

class ApplicantPastJobExperience(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicant_past_job_experiences')  # Link to JobApplication
    job_title = models.CharField(max_length=255)  # Job title
    company_name = models.CharField(max_length=255)  # Company name
    date_started = models.DateField()  # Start date
    date_ended = models.DateField(blank=True, null=True)  # End date

    def __str__(self):
        return f"{self.job_title} at {self.company_name} for {self.job_application}"
