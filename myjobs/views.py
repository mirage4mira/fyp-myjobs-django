import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import connection
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile, Skill, JobExperience, PreferredJobClassification, Employer, Job, LanguageProficiency
from django.core.files.storage import FileSystemStorage


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
            return redirect('signin')
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return redirect('register')
    return render(request, 'myjobs/register.html')

def setup(request):
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
    jobs = Job.objects.select_related('company').all()  # Fetch all jobs with related company details
    jobs_with_company = []
    for job in jobs:
        encoded_image = None
        if job.company.company_logo:  # Assuming the Job model has an 'image' field
            with open(job.company.company_logo.path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        jobs_with_company.append({
            'job': job,
            'company_name': job.company.company_name,
            'company_logo': job.company.company_logo if job.company.company_logo else None,
            'encoded_image': encoded_image  # Include encoded image
        })
    return render(request, 'myjobs/jobs.html', {'jobs': jobs_with_company})

def employer_setup(request):
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

def trace_application(request, job_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to sign in to trace applications.')
        return redirect('signin')

    try:
        job = Job.objects.get(id=job_id, company__user=request.user)  # Ensure the job belongs to the logged-in employer
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to view applications.')
        return redirect('employer_dashboard')

    applications = job.application_set.all()  # Assuming a related name `application_set` exists for applications
    return render(request, 'myjobs/trace_application.html', {'job': job, 'applications': applications})

def apply_job(request, job_id):
    if request.method == 'POST':
        job_id = job_id
        applicant_name = request.POST.get('applicant_name')
        applicant_email = request.POST.get('applicant_email')
        applicant_resume = request.FILES.get('applicant_resume')

        # Save the uploaded resume file
        fs = FileSystemStorage()
        resume_filename = fs.save(applicant_resume.name, applicant_resume)

        # Logic to save application details (e.g., save to database)
        # Example:
        # JobApplication.objects.create(
        #     job_id=job_id,
        #     name=applicant_name,
        #     email=applicant_email,
        #     resume=resume_filename
        # )

        # Redirect to a success page or return a success message
        return HttpResponse("Application submitted successfully!")

    elif request.method == 'GET':
        try:
            job = Job.objects.get(id=job_id)  # Fetch the job details
        except Job.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('jobs')  # Redirect to jobs page if job does not exist

        user_profile = None
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)  # Fetch the user's profile
                # Pre-fill application form with user profile details if available
                if user_profile:
                    skills = user_profile.skills.all()  # Fetch user's skills
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
                'languages': languages,
                'job_experiences': job_experiences  # Pass additional details to the view
            })

    return redirect('jobs')  # Redirect to jobs page if not a valid request method

def logout_view(request):
    logout(request)
    return redirect('home')
