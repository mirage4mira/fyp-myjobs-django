import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import connection
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile, Skill, JobExperience, PreferredJobClassification, Employer, Job, LanguageProficiency, JobApplication, ApplicantSkill, ApplicantPastJobExperience,ApplicantLanguageProficiency
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateformat import format
from datetime import datetime, date

def index(request):
    return render(request, 'myjobs/home.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            login(request, user)  # Logs in the user and sets request.user
            next_url = request.session.pop('next', 'home')  # Get 'next' from session or default to 'home'
            return redirect(next_url)
        else:
            return render(request, 'myjobs/signin.html', {'error': 'Invalid credentials'})

    return render(request, 'myjobs/signin.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Use Django's default User model to create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful!')
            
            # Store username and password in session for one-time use
            request.session['temp_username'] = username
            request.session['temp_password'] = password
            return redirect('signin')  # Redirect to the sign-in page after successful registration
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return redirect('register')
    return render(request, 'myjobs/register.html')

def setup(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to set up your profile.')
        request.session['next'] = 'setup_profile'  # Store the next URL in session
        return redirect('signin')  # Redirect to sign-in page if no user is logged in
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        return redirect('edit_profile')  # Redirect to edit profile if user profile exists
    except UserProfile.DoesNotExist:
        pass  # Continue with setup process if user profile does not exist
    if request.method == 'POST':
        user_id = request.user.id
        skills = request.POST.getlist('skills[]')  # Assuming skills are sent as a list

        # Collect job experience fields properly
        job_titles = request.POST.getlist('job_title[]')
        company_names = request.POST.getlist('company_name[]')
        dates_started = request.POST.getlist('date_started[]')
        dates_ended = request.POST.getlist('date_ended[]')

        bio = request.POST.get('bio')
        home_location = request.POST.get('home_location')  # Assuming home_location is now a select field

        preferred_jobs = request.POST.getlist('preferred_job_classification[]')  # Handles multiple select

        education = request.POST.get('education')

        languages = request.POST.getlist('languages[]')
        proficiencies = request.POST.getlist('proficiencies[]')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Update or create user profile
        user_profile, created = UserProfile.objects.update_or_create(
            user_id=user_id,
            defaults={
                'bio': bio,
                'home_location': home_location,
                'education': education,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number
            }
        )

        print("Languages:", languages)
        print("Proficiencies:", proficiencies)
        print("Preferred Jobs:", preferred_jobs)
        print("Job Titles:", job_titles)
        print("Company Names:", company_names)
        print("Dates Started:", dates_started)
        print("Dates Ended:", dates_ended)
        print("Skills:", skills)

        # Add skills
        for skill_name in skills:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            user_profile.skills.add(skill)

        # Add job experiences
        for title, company, start, end in zip(job_titles, company_names, dates_started, dates_ended):
            JobExperience.objects.create(
                user_profile_id=user_profile.id,
                job_title=title,
                company_name=company,
                date_started=start,
                date_ended=end
            )

        # Add language proficiencies
        for lang, prof in zip(languages, proficiencies):
            LanguageProficiency.objects.create(
                user_profile_id=user_profile.id,
                language=lang,
                proficiency=prof
            )

        # Add preferred jobs
        PreferredJobClassification.objects.filter(user_profile_id=user_profile.id).delete()  # Clear existing entries
        for job in preferred_jobs:
            PreferredJobClassification.objects.create(
                user_profile_id=user_profile.id,
                job_classification=job
            )

        messages.success(request, 'Profile setup completed successfully!')
        return redirect('home')  # Redirect to home after setup completion

    return render(request, 'myjobs/setup_profile.html', {'home_locations': ['Location1', 'Location2', 'Location3']})  # Pass available locations

def edit_profile(request):

    if request.method == 'POST':
        bio = request.POST.get('bio')
        home_location = request.POST.get('home_location')
        education = request.POST.get('education')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Update user profile
        UserProfile.objects.filter(user=request.user).update(
            bio=bio,
            home_location=home_location,
            education=education,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user_profile = UserProfile.objects.get(user=request.user)

        # Update skills
        skills = request.POST.getlist('skills[]')
        user_profile.skills.clear()
        for skill_name in skills:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            user_profile.skills.add(skill)

        # Update job experiences
        JobExperience.objects.filter(user_profile=user_profile).delete()
        job_titles = request.POST.getlist('job_title[]')
        company_names = request.POST.getlist('company_name[]')
        dates_started = request.POST.getlist('date_started[]')
        dates_ended = request.POST.getlist('date_ended[]')
        for title, company, start, end in zip(job_titles, company_names, dates_started, dates_ended):
            JobExperience.objects.create(
                user_profile=user_profile,
                job_title=title,
                company_name=company,
                date_started=start,
                date_ended=end
            )

        # Update language proficiencies
        LanguageProficiency.objects.filter(user_profile=user_profile).delete()
        languages = request.POST.getlist('languages[]')
        proficiencies = request.POST.getlist('proficiencies[]')
        for lang, prof in zip(languages, proficiencies):
            LanguageProficiency.objects.create(
                user_profile=user_profile,
                language=lang,
                proficiency=prof
            )

        # Update preferred job classifications
        PreferredJobClassification.objects.filter(user_profile=user_profile).delete()
        preferred_jobs = request.POST.getlist('preferred_job_classification[]')
        for job in preferred_jobs:
            PreferredJobClassification.objects.create(
                user_profile=user_profile,
                job_classification=job
            )

        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_profile')
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        job_experiences = JobExperience.objects.filter(user_profile=user_profile)
        language_proficiencies = LanguageProficiency.objects.filter(user_profile=user_profile)
        
        skills = user_profile.skills.all()
        skills = [skill.name for skill in skills]

        preferred_job_classifications = PreferredJobClassification.objects.filter(user_profile=user_profile)
        preferred_job_classifications = [job_classification.job_classification for job_classification in preferred_job_classifications]
        print("Job Experiences:", job_experiences)
    except UserProfile.DoesNotExist:
        user_profile = None
        skills = []
        job_experiences = []
        language_proficiencies = []
        preferred_job_classifications = []

    return render(request, 'myjobs/setup_profile.html', {
        'action': 'edit_profile',
        'user_profile': user_profile,
        'skills': skills,
        'job_experiences': job_experiences,
        'language_proficiencies': language_proficiencies,
        'preferred_job_classifications': preferred_job_classifications
    })
    return render(request, 'myjobs/setup_profile.html',{'action': 'edit_profile'})  # Pass action to differentiate between setup and edit

def jobs(request):
    search_keyword = request.GET.get('search', '')  # Get search keyword from query parameters
    if search_keyword:
        jobs_title = Job.objects.filter(title__icontains=search_keyword).select_related('company')
        jobs_description = Job.objects.filter(description__icontains=search_keyword).select_related('company')
        jobs_location = Job.objects.filter(location__icontains=search_keyword).select_related('company')
        jobs_company = Job.objects.filter(company__company_name__icontains=search_keyword).select_related('company')
        
        jobs = list(jobs_title) + list(jobs_description) + list(jobs_location) + list(jobs_company)
    else:
        jobs = Job.objects.select_related('company').all()  # Fetch all jobs with related company details

    jobs = [job for job in jobs if (date.today() - job.date_created_or_renewed).days <= 30]
    
    jobs_with_company = []
    for job in jobs:
        encoded_image = None
        job.job_type = job.job_type.replace('_', ' ').title() if job.job_type else None
        if job.company.company_logo:  # Assuming the Job model has an 'image' field
            with open(job.company.company_logo.path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        jobs_with_company.append({
            'job': job,
            'company_name': job.company.company_name,
            'company_logo': job.company.company_logo if job.company.company_logo else None,
            'encoded_image': encoded_image  # Include encoded image
        })
    
    # Pagination
    paginator = Paginator(jobs_with_company, 15)  # Show 15 jobs per page
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    return render(request, 'myjobs/jobs.html', {'jobs': jobs_page, 'search': search_keyword})

def employer_setup(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to set up your employer profile.')
        request.session['next'] = 'employer_setup_profile'
        return redirect('signin')  # Redirect to sign-in page if no user is logged in
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        phone_number = request.POST.get('phone_number')
        company_bio = request.POST.get('company_bio')
        company_logo = request.FILES.get('company_logo')  # Handle file upload

        # Create or update the Employer profile
        Employer.objects.update_or_create(
            user=request.user,
            defaults={
                'company_name': company_name,
                'company_address': company_address,
                'phone_number': phone_number,
                'company_bio': company_bio,
                'company_logo': company_logo,
            }
        )
        messages.success(request, 'Employer profile setup successfully!')
        return redirect('employer_dashboard')  # Redirect to employer dashboard after setup

    return render(request, 'myjobs/employer_setup_profile.html')

def employer_dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to access the employer dashboard.')
        request.session['next'] = 'employer_dashboard'  # Store the next URL in session
        return redirect('signin')  # Redirect to sign-in page if no user is logged in

    try:
        # Attempt to get the Employer object for the logged-in user
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        employer = None

    if not employer:
        # Handle case where employer does not exist
        messages.error(request, 'Employer profile not found. Please set up your profile.')
        return redirect('employer_setup_profile')  # Redirect to setup profile if Employer does not exist

    # Fetch jobs posted by the employer
    jobs = Job.objects.filter(company=employer)
    # Count the number of applications for each job

    for job in jobs:
        job.application_count = JobApplication.objects.filter(job=job).count()
        # Ensure both are aware datetime objects
        if isinstance(job.date_created_or_renewed, date) and not isinstance(job.date_created_or_renewed, datetime):
            job_created_datetime = datetime.combine(job.date_created_or_renewed, datetime.min.time())
        else:
            job_created_datetime = job.date_created_or_renewed

        if timezone.is_naive(job_created_datetime):
            job_created_datetime = make_aware(job_created_datetime)

        job.number_of_days_since_posted = (timezone.now() - job_created_datetime).days
        job.listing_days_allowed = 30  - job.number_of_days_since_posted
    return render(request, 'myjobs/employer_dashboard.html', {'employer': employer, 'jobs': jobs})

@csrf_protect
def create_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        job_location = request.POST.get('job_location')
        job_salary = request.POST.get('job_salary')
        number_of_candidates = request.POST.get('number_of_candidates')
        required_education = request.POST.get('required_education')
        required_experience_years = request.POST.get('required_experience_years')
        
        # Get the company ID from the logged-in user's employer profile
        try:
            employer = Employer.objects.get(user=request.user)
            company_id = employer.id
        except Employer.DoesNotExist:
            messages.error(request, 'Employer profile not found. Please set up your profile.')
            return redirect('employer_setup_profile')

        Job.objects.create(
            title=job_title,
            description=job_description,
            location=job_location,
            salary=job_salary,
            number_of_candidates=number_of_candidates,
            required_education=required_education,
            required_experience_years=required_experience_years,
            company_id=company_id  # Insert company ID
        )
        return redirect('employer_dashboard')  # Add trailing slash
    return render(request, 'myjobs/employer_dashboard.html')

@csrf_protect
def edit_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, company__user=request.user)  # Ensure the job belongs to the logged-in employer
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to edit this job.')
        return redirect('employer_dashboard')

    if request.method == 'POST':
        job.title = request.POST.get('job_title')
        job.description = request.POST.get('job_description')
        job.location = request.POST.get('job_location')
        job.salary = request.POST.get('job_salary')
        job.number_of_candidates = request.POST.get('number_of_candidates')
        job.required_education = request.POST.get('required_education')
        job.required_experience_years = request.POST.get('required_experience_years')
        job.save()
        messages.success(request, 'Job updated successfully!')
        return redirect('employer_dashboard')

    return render(request, 'myjobs/employer_edit_job.html', {'job': job})

@require_POST
def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, company__user=request.user)  # Ensure the job belongs to the logged-in employer
        job.delete()
        messages.success(request, 'Job deleted successfully!')
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to delete this job.')
    return redirect('employer_dashboard')  # Add trailing slash

@require_POST
def renew_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, company__user=request.user)  # Ensure the job belongs to the logged-in employer
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to renew this job.')
        return redirect('employer_dashboard')

    job.date_created_or_renewed = timezone.now()  # Update the renewal date to the current time
    job.save()
    messages.success(request, 'Job renewed successfully!')
    return redirect('employer_dashboard')
    
def trace_application(request, job_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to trace applications.')
        return redirect('signin')

    try:
        job = Job.objects.get(id=job_id, company__user=request.user)  # Ensure the job belongs to the logged-in employer
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to view applications.')
        return redirect('employer_dashboard')

    applications = JobApplication.objects.filter(job=job)
    status_choices = JobApplication._meta.get_field('status').choices  # Correctly retrieve status choices
    return render(request, 'myjobs/trace_application.html', {'job': job, 'applications': applications, 'status_choices': status_choices})

def delete_application(request, job_id, application_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to delete applications.')
        return redirect('signin')

    try:
        application = JobApplication.objects.get(id=application_id, job__id=job_id, job__company__user=request.user)  # Ensure the application belongs to the logged-in employer
        application.delete()
        messages.success(request, 'Application deleted successfully!')
    except JobApplication.DoesNotExist:
        messages.error(request, 'Application not found or you do not have permission to delete this application.')
    return redirect('employer_trace_application', job_id=job_id)  # Include job_id in the redirect

def view_application(request, job_id, application_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to view applications.')
        return redirect('signin')

    try:
        application = JobApplication.objects.get(id=application_id, job__id=job_id, job__company__user=request.user)  # Ensure the application belongs to the logged-in employer
    except JobApplication.DoesNotExist:
        messages.error(request, 'Application not found or you do not have permission to view this application.')
        return redirect('employer_dashboard')

    return render(request, 'myjobs/view_application.html', {'application': application})

@login_required
def view_applications(request, job_id):
    # Logic to fetch and display applications for the given job_id
    applications = []  # Replace with actual query to fetch applications
    return render(request, 'employer/view_applications.html', {'applications': applications, 'job_id': job_id})

def apply_job(request, job_id):

    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to apply for this job.')
        request.session['next'] = f'/jobs/{job_id}/apply'
        return redirect('signin')
    
    existing_application = JobApplication.objects.filter(user_id=request.user.id, job_id=job_id).first()
    if existing_application:
        messages.error(request, "You have already submitted an application for this job.")
        return redirect(request.META.get('HTTP_REFERER', 'jobs'))
    
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        applicant_resume = request.FILES.get('resume')
        phone_number = request.POST.get('phone_number')
        home_location = request.POST.get('home_location')  # Assuming home_location is now a select fielde
        education = request.POST.get('education')  # Assuming education is now a select field
        applicant_bio = request.POST.get('bio')
        skills = request.POST.getlist('skills[]')
        job_titles = request.POST.getlist('job_title[]')
        company_names = request.POST.getlist('company_name[]')
        dates_started = request.POST.getlist('date_started[]')
        dates_ended = request.POST.getlist('date_ended[]')
        languages = request.POST.getlist('languages[]')
        proficiencies = request.POST.getlist('proficiencies[]')

        # Check if the user has already applied for the job

        # Save the uploaded resume file to the 'resumes' folder
        fs = FileSystemStorage(location='resumes')
        resume_filename = fs.save(applicant_resume.name, applicant_resume)  # Use the file's name

        # Save application details
        job_application = JobApplication.objects.create(
            job_id=job_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            resume=resume_filename,
            phone_number=phone_number,
            home_location=home_location,  # Assuming home_location is now a select field
            education=education,  # Assuming education is now a select field
            bio=applicant_bio,  # Assuming education is now a select field
            user_id=request.user.id,  # Assuming the user is logged in and has an ID
        )

        # Save applicant skills
        for skill_name in skills:
            ApplicantSkill.objects.create(
                job_application=job_application,
                name=skill_name
            )

        # Save applicant past job experiences
        for title, company, start, end in zip(job_titles, company_names, dates_started, dates_ended):
            ApplicantPastJobExperience.objects.create(
                job_application=job_application,
                job_title=title,
                company_name=company,
                date_started=start,
                date_ended=end
            )

        # Save applicant language proficiencies
        for lang, prof in zip(languages, proficiencies):
            ApplicantLanguageProficiency.objects.create(
                job_application=job_application,
                language=lang,
                proficiency=prof
            )

        messages.success(request, "Application submitted successfully!")
        return redirect('jobs')
        return HttpResponse("Application submitted successfully!")

    elif request.method == 'GET':
        try:
            job = Job.objects.get(id=job_id)  # Fetch the job details
            job.job_type = job.job_type.replace('_', ' ').title() if job.job_type else None
        except Job.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('jobs')  # Redirect to jobs page if job does not exist

        user_profile = None
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)  # Fetch the user's profile
                # Pre-fill application form with user profile details if available
                if user_profile:
                    skills = Skill.objects.filter(user_profile_id = user_profile.id)
                    skills = [skill.name for skill in skills]
                    # print("User Skills:", [skill.name for skill in skills])
                    languages = LanguageProficiency.objects.filter(user_profile_id = user_profile.id)  # Assuming a related name for language proficiency
                    job_experiences = JobExperience.objects.filter(user_profile_id = user_profile.id)  # Fetch user's job experiences
                    # print("Languages:", [language.language_name for language in languages])
                    # print("Job Experiences:", [experience.description for experience in job_experiences])
                else:
                    skills = []
                    languages = []
                    job_experiences = []

            except UserProfile.DoesNotExist:
                pass  # Handle case where user profile does not exist

            return render(request, 'myjobs/apply_job.html', {
                'job': job,
                'user_profile': user_profile,
                'skills': skills,
                'language_proficiencies': languages,
                'job_experiences': job_experiences  # Pass additional details to the view
            })

    return redirect('job')  # Redirect to jobs page if not a valid request method

def logout_view(request):
    logout(request)
    return redirect('home')

def change_application_status(request,job_id, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication._meta.get_field('status').choices):
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    return redirect(request.META.get('HTTP_REFERER', 'myjobs:trace_application'))
