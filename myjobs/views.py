from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import connection
from django.contrib.auth import logout

def index(request):
    return render(request, 'myjobs/home.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM users WHERE email = %s", [email])
            user = cursor.fetchone()

        if user and check_password(password, user[1]):
            request.session['user_id'] = user[0]
            return redirect('home')  # Replace 'home' with your desired redirect URL
        else:
            return render(request, 'myjobs/signin.html', {'error': 'Invalid email or password'})

    return render(request, 'myjobs/signin.html')

def register(request):
    if request.method == 'POST':
        # Print data from the request for debugging
        # raise Exception(str(request))
        
    
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Hash the password
        hashed_password = make_password(password)
        
        # Insert into the database
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (username, email, password)
                    VALUES (%s, %s, %s)
                """, [username, email, hashed_password])
            messages.success(request, 'Registration successful!')
            return redirect('signin')
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return redirect('register')
    return render(request, 'myjobs/register.html')

def setup(request):
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
