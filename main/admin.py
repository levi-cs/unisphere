from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import User
from django.forms.widgets import TimeInput

from .models import (
    Course, Semester, Student, Teacher, Subject,
    Attendance, Material, Notice, Announcement,
    Timetable, OTPVerification, Complaint
)

# ==============================
# 🔹 STUDENT RESOURCE (FINAL FIXED)
# ==============================
class StudentResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        email = row.get('email')
        student_id = row.get('student_id')

        # 🔹 AUTO EMAIL
        if not email and student_id:
            email = f"{student_id}@unisphere.com"
            row['email'] = email

        # 🔹 CREATE USER
        if email:
            user, created = User.objects.get_or_create(
                username=student_id,
                defaults={'email': email}
            )

            if created:
                user.set_password("student123")
                user.save()

        # 🔹 COURSE NAME → OBJECT
        course_name = row.get('course')
        if course_name:
            course, _ = Course.objects.get_or_create(
                name=course_name.strip()
            )
            row['course'] = course.id

        # 🔹 SEMESTER NAME → NUMBER
        sem_name = row.get('semester')
        if sem_name:
            roman_map = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4,
                'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8
            }

            sem_num = None
            sem_name = sem_name.upper()

            for key in sorted(roman_map.keys(), key=len, reverse=True):
                 if key in sem_name:
                    sem_num = roman_map[key]
                    break

            if sem_num:
                semester, _ = Semester.objects.get_or_create(number=sem_num)
                row['semester'] = semester.id

    # 🔥 THIS FIXES "Student has no user"
    def after_import_instance(self, instance, new, **kwargs):
        if not instance.user:
            user = User.objects.filter(username=instance.email).first()
            if user:
                instance.user = user
                instance.save()

    class Meta:
        model = Student
        import_id_fields = ('student_id',)
        fields = ('name', 'student_id', 'email', 'course', 'semester')


# ==============================
# 🔹 TEACHER RESOURCE
# ==============================
class TeacherResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        email = row.get('email')
        teacher_id = row.get('teacher_id')

        if not email and teacher_id:
            email = f"{teacher_id}@unisphere.com"
            row['email'] = email

        if email:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'email': email}
            )

            if created:
                user.set_password("teacher123")
                user.save()

    def after_import_instance(self, instance, new, **kwargs):
        if not instance.user:
            user = User.objects.filter(username=instance.email).first()
            if user:
                instance.user = user
                instance.save()

    class Meta:
        model = Teacher
        import_id_fields = ('teacher_id',)
        fields = ('name', 'teacher_id', 'email', 'department')


# ==============================
# 🔹 STUDENT ADMIN
# ==============================
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ['name', 'student_id', 'email', 'course', 'semester']
    search_fields = ['name', 'student_id', 'email']
    list_filter = ['course', 'semester']


# ==============================
# 🔹 TEACHER ADMIN
# ==============================
@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = ['name', 'teacher_id', 'email', 'department']
    search_fields = ['name', 'teacher_id']


# ==============================
# 🔹 OTHER ADMINS
# ==============================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'semester', 'teacher']
    list_filter = ['semester']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'total_classes', 'attended', 'percentage']
    list_filter = ['subject__semester']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'uploaded']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'posted_by', 'created']
    list_filter = ['priority']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'created']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['student__name', 'subject']


from django import forms

class TimetableAdminForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'
        widgets = {
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'}),
        }


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    form = TimetableAdminForm
    list_display = ['subject', 'day', 'start_time', 'end_time', 'room', 'semester']
    list_filter = ['day', 'semester']


admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(OTPVerification)
