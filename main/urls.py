from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARD
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # SECTIONS
    path('subjects/', views.subjects_view, name='subjects'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('materials/', views.materials_view, name='materials'),
    path('notices/', views.notices_view, name='notices'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('complaints/', views.complaints_view, name='complaints'),
    path('profile/', views.profile_view, name='profile'),
    path('results/', views.results_view, name='results'),

    # TEACHER
    path('post-announcement/', views.post_announcement_view, name='post_announcement'),
    path('upload-materials/', views.upload_materials_zip, name='upload_materials'),
    path('feedback/', views.submit_feedback, name='feedback'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
]
