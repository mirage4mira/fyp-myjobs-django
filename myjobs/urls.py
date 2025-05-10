import os  # Import os for path joining
from django.urls import path, re_path  # Import re_path for custom static file serving
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
from .views import edit_job, trace_application, apply_job,renew_job ,delete_job, view_applications  # Import the new view
from django.views.static import serve  # Import the serve view


urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('setup-profile/', login_required(views.setup), name='setup_profile'),
    path('edit-profile/', login_required(views.edit_profile), name='edit_profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:job_id>/apply', views.apply_job, name='apply_job'),
    path('employer/setup-profile/', login_required(views.employer_setup), name='employer_setup_profile'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('logout', login_required(views.logout_view), name='logout'),
    path('employer/job/create', login_required(views.create_job), name='employer_create_job'),
    path('employer/job/<int:job_id>/edit/', login_required(edit_job), name='employer_edit_job'),
    path('employer/job/<int:job_id>/application/<int:application_id>/view', login_required(views.view_application), name='employer_view_application'),
    path('employer/job/<int:job_id>/application/<int:application_id>/change-status/', views.change_application_status, name='change_application_status'),  # Add the new route
    path('employer/job/<int:job_id>/application/', login_required(trace_application), name='employer_trace_application'),
    path('employer/job/<int:job_id>/application/<int:application_id>/delete', login_required(views.delete_application), name='employer_delete_application'),
    path('employer/job/<int:job_id>/delete/', login_required(delete_job), name='employer_delete_job'),
    path('employer/job/<int:job_id>/renew/', login_required(renew_job), name='employer_renew_job'),
    # path('employer/job/<int:job_id>/applications/', login_required(view_applications), name='employer_view_applications'),  # Add the new route
    re_path(r'^resumes/(?P<path>.*)$', login_required(serve), {'document_root': os.path.join(settings.BASE_DIR, 'resumes')}, name='view_resumes'),
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
