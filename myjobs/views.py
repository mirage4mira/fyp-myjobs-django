from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import connection
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

def index(request):
    return render(request, 'myjobs/home.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            request.session['user_id'] = user.id
            login(request, user)  # Logs in the user and sets request.user
            return redirect('home')
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
    if request.method == 'POST':
        # Logic to update profile completion status
        # Example: Update `profile_completed` to True in the database
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users SET profile_completed = TRUE WHERE id = %s
            """, [request.user.id])
        return redirect('home')  # Redirect to home after setup completion

    return render(request, 'myjobs/setup_profile.html')

def jobs(request):
    # Add logic to fetch job details if needed
    return render(request, 'myjobs/jobs.html')

def employer_login(request):
    return render(request, 'myjobs/employer_login.html')

def employer_register(request):
    return render(request, 'myjobs/employer_register.html')

def employer_setup(request):
    # Logic for employer setup profile
    return render(request, 'myjobs/employer_setup_profile.html')

def employer_dashboard(request):
    return render(request, 'myjobs/employer_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('/')
