from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARD (single entry point)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # FEATURES (non-section actions)
    path('post-announcement/', views.post_announcement_view, name='post_announcement'),
    path('upload-materials/', views.upload_materials_zip, name='upload_materials'),

    # FEEDBACK (legacy / optional separate pages)
    path('feedback/', views.submit_feedback, name='feedback'),
    path('post-notice/', views.post_notice, name='post_notice'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
]
