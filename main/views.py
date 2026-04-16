import random
import string
import zipfile
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files import File

from .models import (
    Student, Teacher, Subject, Attendance, Material,
    Notice, Announcement, Timetable, Semester, Course,
    Complaint, OTPVerification
)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def get_role(user):
    if user.is_superuser:
        return 'admin'
    if hasattr(user, 'teacher'):
        return 'teacher'
    if hasattr(user, 'student'):
        return 'student'
    return 'unknown'


def send_otp(email):
    otp = ''.join(random.choices(string.digits, k=6))
    OTPVerification.objects.filter(email=email).delete()
    OTPVerification.objects.create(email=email, otp=otp)

    try:
        send_mail(
            subject='UniSphere — OTP Code',
            message=f'Your OTP is: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
    except Exception:
        pass

    return otp


# ─────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        tab = request.POST.get('tab')
        password = request.POST.get('password')

        if tab == 'admin':
            username = request.POST.get('username')
            user = authenticate(request, username=username, password=password)

            if user and user.is_superuser:
                login(request, user)
                return redirect('dashboard')

            messages.error(request, 'Invalid admin login')

        elif tab == 'teacher':
            teacher_id = request.POST.get('student_id')

            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                user = authenticate(request, username=teacher.user.username, password=password)

                if user:
                    login(request, user)
                    return redirect('dashboard')
            except:
                pass

            messages.error(request, 'Invalid teacher login')

        else:
            student_id = request.POST.get('student_id')

            try:
                student = Student.objects.get(student_id=student_id)
                user = authenticate(request, username=student.user.username, password=password)

                if user:
                    login(request, user)
                    return redirect('dashboard')
            except:
                pass

            messages.error(request, 'Invalid student login')

    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────
# CONTEXT
# ─────────────────────────────────────────
def base_context(request):
    user = request.user
    role = get_role(user)

    ctx = {'user': user, 'role': role}

    if role == 'student':
        ctx['student'] = user.student
    elif role == 'teacher':
        ctx['teacher'] = user.teacher

    return ctx


# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────
@login_required
def dashboard_view(request):
    ctx = base_context(request)

    ctx['section'] = 'overview'
    ctx['notices'] = Notice.objects.all()[:5]
    ctx['announcements'] = Announcement.objects.all()[:3]

    if ctx['role'] == 'student':
        student = ctx['student']

        # Subjects
        ctx['subjects'] = Subject.objects.filter(
            semester=student.semester
        )

        # Attendance
        attendance_qs = Attendance.objects.filter(student=student)
        ctx['attendance_data'] = attendance_qs

        if attendance_qs.exists():
            total = sum(a.percentage for a in attendance_qs)
            ctx['avg_attendance'] = round(total / attendance_qs.count())
        else:
            ctx['avg_attendance'] = 0

        # Materials
        ctx['materials_count'] = Material.objects.filter(
            subject__semester=student.semester
        ).count()

    elif ctx['role'] == 'teacher':
        ctx['subjects'] = Subject.objects.filter(
            teacher=ctx['teacher']
        )

    return render(request, 'main/dashboard.html', ctx)


@login_required
def complaints_view(request):
    ctx = base_context(request)
    ctx['section'] = 'complaints'

    if ctx['role'] != 'student':
        messages.error(request, "Only students can register complaints.")
        return redirect('dashboard')

    if request.method == 'POST':
        subject = (request.POST.get('subject') or '').strip()
        category = request.POST.get('category') or 'other'
        description = (request.POST.get('description') or '').strip()

        if not subject or not description:
            messages.error(request, "Subject and description are required.")
        else:
            Complaint.objects.create(
                student=ctx['student'],
                subject=subject,
                category=category,
                description=description,
            )
            messages.success(request, "Complaint submitted successfully.")
            return redirect('complaints')

    ctx['complaints'] = Complaint.objects.filter(student=ctx['student'])
    ctx['complaint_categories'] = Complaint.CATEGORY_CHOICES
    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────
@login_required
def subjects_view(request):
    ctx = base_context(request)
    ctx['section'] = 'subjects'

    if ctx['role'] == 'student':
        ctx['subjects'] = Subject.objects.filter(
            semester=ctx['student'].semester
        )

    elif ctx['role'] == 'teacher':
        ctx['subjects'] = Subject.objects.filter(
            teacher=ctx['teacher']
        )

    else:
        ctx['subjects'] = Subject.objects.all()

    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# ATTENDANCE
# ─────────────────────────────────────────
@login_required
def attendance_view(request):
    ctx = base_context(request)
    ctx['section'] = 'attendance'

    if ctx['role'] == 'student':
        ctx['attendance_data'] = Attendance.objects.filter(
            student=ctx['student']
        )

    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# MATERIALS
# ─────────────────────────────────────────
@login_required
def materials_view(request):
    ctx = base_context(request)
    ctx['section'] = 'materials'

    if ctx['role'] == 'student':
        ctx['materials'] = Material.objects.filter(
            subject__semester=ctx['student'].semester
        )

    elif ctx['role'] == 'teacher':
        ctx['materials'] = Material.objects.filter(
            subject__teacher=ctx['teacher']
        )

    else:
        ctx['materials'] = Material.objects.all()

    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# NOTICES
# ─────────────────────────────────────────
@login_required
def notices_view(request):
    ctx = base_context(request)
    ctx['section'] = 'notices'
    ctx['notices'] = Notice.objects.all()

    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# TIMETABLE
# ─────────────────────────────────────────
from collections import defaultdict

@login_required
def timetable_view(request):
    ctx = base_context(request)
    ctx['section'] = 'timetable'

    if ctx['role'] == 'student':
        entries = Timetable.objects.filter(
            semester=ctx['student'].semester
        )

    elif ctx['role'] == 'teacher':
        entries = Timetable.objects.filter(
            subject__teacher=ctx['teacher']
        )

    else:
        entries = Timetable.objects.all()

    # 🔥 STEP 1: unique sorted time slots
    timeslots = sorted(set([(e.start_time, e.end_time) for e in entries]))

    # 🔥 STEP 2: create matrix
    timetable_matrix = defaultdict(dict)

    for e in entries:
        key = (e.start_time, e.end_time)
        timetable_matrix[key][e.day] = e

    ctx['timeslots'] = timeslots
    ctx['timetable_matrix'] = timetable_matrix
    ctx['days'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return render(request, 'main/dashboard.html', ctx)

# ─────────────────────────────────────────
# ANNOUNCEMENTS
# ─────────────────────────────────────────
@login_required
def announcements_view(request):
    ctx = base_context(request)
    ctx['section'] = 'announcements'
    ctx['announcements'] = Announcement.objects.all()

    return render(request, 'main/dashboard.html', ctx)


# ─────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────
@login_required
def profile_view(request):
    ctx = base_context(request)
    ctx['section'] = 'profile'

    return render(request, 'main/dashboard.html', ctx)
# ─────────────────────────────────────────
# SIGNUP
# ─────────────────────────────────────────
def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        course_name = request.POST.get('course')
        sem_num = request.POST.get('semester')
        password = request.POST.get('password')

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "Student already exists")
            return redirect('signup')

        # Save temporarily
        request.session['signup_data'] = {
            'name': name,
            'student_id': student_id,
            'email': email,
            'course_name': course_name,
            'sem_num': sem_num,
            'password': password,
        }

        send_otp(email)
        return redirect('verify_otp')

    return render(request, 'main/signup.html')


# ─────────────────────────────────────────
# VERIFY OTP
# ─────────────────────────────────────────
def verify_otp_view(request):
    data = request.session.get('signup_data')

    if not data:
        return redirect('signup')

    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            otp_obj = OTPVerification.objects.get(
                email=data['email'], otp=otp, is_used=False
            )
            otp_obj.is_used = True
            otp_obj.save()

            # Create user
            user = User.objects.create_user(
                username=data['student_id'],
                email=data['email'],
                password=data['password']
            )

            course, _ = Course.objects.get_or_create(name=data['course_name'])
            semester, _ = Semester.objects.get_or_create(number=int(data['sem_num']))

            Student.objects.create(
                user=user,
                name=data['name'],
                student_id=data['student_id'],
                email=data['email'],
                course=course,
                semester=semester,
            )

            del request.session['signup_data']
            messages.success(request, "Account created successfully")
            return redirect('login')

        except:
            messages.error(request, "Invalid OTP")

    return render(request, 'main/verify_otp.html')


# ─────────────────────────────────────────
# FORGOT PASSWORD
# ─────────────────────────────────────────
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            send_otp(email)
            request.session['reset_email'] = email
            return redirect('reset_password')

        messages.error(request, "Email not found")

    return render(request, 'main/forgot_password.html')


# ─────────────────────────────────────────
# RESET PASSWORD
# ─────────────────────────────────────────
def reset_password_view(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')

        try:
            otp_obj = OTPVerification.objects.get(
                email=email, otp=otp, is_used=False
            )
            otp_obj.is_used = True
            otp_obj.save()

            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            del request.session['reset_email']
            messages.success(request, "Password reset successful")
            return redirect('login')

        except:
            messages.error(request, "Invalid OTP")

    return render(request, 'main/reset_password.html')


# ─────────────────────────────────────────
# TEACHER ANNOUNCEMENT
# ─────────────────────────────────────────
@login_required
def post_announcement_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if hasattr(request.user, 'teacher'):
            Announcement.objects.create(
                title=title,
                content=content,
                teacher=request.user.teacher
            )
            messages.success(request, "Announcement posted")

    return redirect('announcements')

import zipfile
import os
from django.conf import settings
from django.core.files import File

@login_required
def upload_materials_zip(request):
    if request.method == 'POST':
        zip_file = request.FILES.get('zip_file')
        subject_id = request.POST.get('subject')

        if not zip_file or not subject_id:
            messages.error(request, "Missing file or subject")
            return redirect('materials')

        subject = Subject.objects.get(id=subject_id)

        # Save zip temporarily
        zip_path = os.path.join(settings.MEDIA_ROOT, zip_file.name)
        with open(zip_path, 'wb+') as f:
            for chunk in zip_file.chunks():
                f.write(chunk)

        # Extract zip
        extract_folder = os.path.join(settings.MEDIA_ROOT, 'materials_temp')
        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Save each file as Material
        for file_name in os.listdir(extract_folder):
            file_path = os.path.join(extract_folder, file_name)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    material = Material.objects.create(
                        title=file_name,
                        subject=subject
                    )
                    material.file.save(file_name, File(f), save=True)

        messages.success(request, "Materials uploaded successfully")
        return redirect('materials')

    ctx = base_context(request)
    ctx['subjects'] = Subject.objects.all()
    return render(request, 'main/upload_materials.html', ctx)

# ==============================
# STUDENT: SUBMIT FEEDBACK
# ==============================
@login_required
def submit_feedback(request):
    if not hasattr(request.user, 'student'):
        return redirect('dashboard')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Complaint.objects.create(
            student=request.user.student,
            subject=subject,
            message=message
        )

        messages.success(request, "Feedback submitted successfully")
        return redirect('feedback')

    ctx = base_context(request)
    return render(request, 'main/feedback.html', ctx)


# ==============================
# TEACHER: VIEW FEEDBACK
# ==============================
@login_required
def view_feedback(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('dashboard')

    complaints = Complaint.objects.all().order_by('-created')

    ctx = base_context(request)
    ctx['complaints'] = complaints
    return render(request, 'main/view_feedback.html', ctx)

@login_required
def results_view(request):
    ctx = base_context(request)
    ctx['section'] = 'results'   # 🔥 THIS IS THE KEY
    return render(request, 'main/dashboard.html', ctx)