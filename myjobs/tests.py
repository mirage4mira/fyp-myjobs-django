from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myjobs.models import UserProfile, Employer, Job, JobApplication

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.employer = Employer.objects.create(user=self.user, company_name="Test Company")
        self.user_profile = UserProfile.objects.create(  # Ensure profile setup is complete
            user=self.user,
            bio="Test Bio",
            home_location="Test Location",
            education="Bachelor",
            phone_number="1234567890"
        )
        self.job = Job.objects.create(
            title="Test Job",
            description="Test Description",
            location="Test Location",
            salary=50000,
            company=self.employer,
            number_of_candidates=10,  # Add default value for this field
            required_experience_years=1,        
        )

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_signin_view(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

    def test_setup_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('setup_profile'))
        self.assertEqual(response.status_code, 302)  # Update expected status code to match redirect behavior

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'bio': 'Test Bio',
            'home_location': 'Test Location',
            'education': 'Bachelor',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful profile update

    def test_jobs_view(self):
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)

    def test_employer_setup_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('employer_setup_profile'), {
            'company_name': 'New Company',
            'company_address': '123 Test St',
            'phone_number': '1234567890',
            'company_bio': 'Test Bio'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful setup

    def test_employer_dashboard_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 200)  # Expect 200 after profile setup

    def test_create_job_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('employer_create_job'), {
            'job_title': 'New Job',
            'job_description': 'Job Description',
            'job_location': 'Job Location',
            'job_salary': 60000,
            'job_category': 'IT',
            'number_of_candidates': 5,
            'required_education': 'Bachelor',
            'required_experience_years': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful job creation

    def test_edit_job_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('employer_edit_job', args=[self.job.id]), {
            'job_title': 'Updated Job',
            'job_description': 'Updated Description',
            'job_location': 'Updated Location',
            'job_salary': 70000,
            'number_of_candidates': 10,
            'required_education': 'Master',
            'required_experience_years': 3
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful job update

    def test_delete_job_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('employer_delete_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful job deletion

    def test_renew_job_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('employer_renew_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful job renewal

    def test_apply_job_view(self):
        self.client.login(username='testuser', password='testpassword')
        with open('test_resume.pdf', 'w') as f:  # Create a dummy file for testing
            f.write('Dummy resume content')
        with open('test_resume.pdf', 'rb') as resume_file:
            response = self.client.post(reverse('apply_job', args=[self.job.id]), {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'testuser@example.com',
                'phone_number': '1234567890',
                'home_location': 'Test Location',
                'education': 'Bachelor',
                'bio': 'Test Bio',
                'resume': resume_file  # Include the resume file in the POST data
            })
        self.assertEqual(response.status_code, 302)  # Redirect after successful application

    def test_trace_application_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('employer_trace_application', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)  # Expect 200 after profile setup

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_change_application_status_view(self):
        application = JobApplication.objects.create(job=self.job, user=self.user, status='Pending')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('change_application_status', args=[self.job.id, application.id]), {
            'status': 'Confirmed'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after status change
