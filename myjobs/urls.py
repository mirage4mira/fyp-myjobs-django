from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('setup-profile/', views.setup, name='setup_profile'),
    path('jobs/', views.jobs, name='job'),
    path('employer-login/', views.employer_login, name='employer_login'),
    path('employer-register/', views.employer_register, name='employer_register'),
    path('employer-setup-profile/', views.employer_setup, name='employer_setup_profile'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('logout', views.logout_view, name='logout'),
]