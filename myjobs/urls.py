from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
from .views import edit_job, trace_application, apply_job,delete_job  # Import the new view

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('setup-profile/', views.setup, name='setup_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('jobs/', views.jobs, name='job'),
    path('employer/setup-profile/', views.employer_setup, name='employer_setup_profile'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('logout', views.logout_view, name='logout'),
    path('employer/job/create', views.create_job, name='employer_create_job'),
    path('employer/job/<int:job_id>/edit/', edit_job, name='employer_edit_job'),
    path('employer/job/<int:job_id>/trace/', trace_application, name='employer_trace_application'),
    path('employer/job/<int:job_id>/delete/', delete_job, name='employer_delete_job'),  # Ensure trailing slash
    path('jobs/<int:job_id>/apply', apply_job, name='apply_job'),  # Add the new route
]

#path('employer-login/', views.employer_login, name='employer_login'),
#path('employer-register/', views.employer_register, name='employer_register'),

# if settings.DEBUG:
#     from django.urls import re_path
#     from django.views.static import serve

#     urlpatterns += [
#         re_path(r'^(?!employer/dashboard).*$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
