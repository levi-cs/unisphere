from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Semester {self.number}"


# ==============================
# 🔹 STUDENT (FINAL FIX)
# ==============================
class Student(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=True, blank=True)
    name       = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    email      = models.EmailField()
    course     = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    semester   = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # 🔥 AUTO CREATE USER (MAIN FIX)
        if not self.user:
            user, created = User.objects.get_or_create(
                username=self.email,
                defaults={'email': self.email}
            )

            if created:
                user.set_password("student123")
                user.save()

            self.user = user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


# ==============================
# 🔹 TEACHER (ALSO FIXED)
# ==============================
class Teacher(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', null=True, blank=True)
    name        = models.CharField(max_length=100)
    teacher_id  = models.CharField(max_length=50, unique=True)
    email       = models.EmailField()
    department  = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.user:
            user, created = User.objects.get_or_create(
                username=self.email,
                defaults={'email': self.email}
            )

            if created:
                user.set_password("teacher123")
                user.save()

            self.user = user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.teacher_id})"


class Subject(models.Model):
    name     = models.CharField(max_length=100)
    code     = models.CharField(max_length=20, blank=True)
    credits  = models.IntegerField(default=3)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher  = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Attendance(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject        = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_classes  = models.IntegerField(default=0)
    attended       = models.IntegerField(default=0)

    @property
    def percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.attended / self.total_classes) * 100)

    @property
    def status(self):
        p = self.percentage
        if p >= 85:
            return 'safe'
        elif p >= 75:
            return 'good'
        elif p >= 60:
            return 'warning'
        return 'danger'

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} ({self.percentage}%)"


class Material(models.Model):
    title       = models.CharField(max_length=200)
    file        = models.FileField(upload_to='materials/')
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE)
    uploaded    = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Notice(models.Model):
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
    ]

    title     = models.CharField(max_length=200)
    content   = models.TextField(blank=True)
    priority  = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    created   = models.DateTimeField(auto_now_add=True)
    posted_by = models.CharField(max_length=100, default='Admin')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title   = models.CharField(max_length=200)
    content = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('attendance', 'Attendance'),
        ('facility', 'Facility'),
        ('exam', 'Exam'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.student.student_id} - {self.subject}"


class OTPVerification(models.Model):
    email      = models.EmailField()
    otp        = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.email}"


class Timetable(models.Model):
    DAYS = [
        ('Monday','Monday'), ('Tuesday','Tuesday'), ('Wednesday','Wednesday'),
        ('Thursday','Thursday'), ('Friday','Friday'), ('Saturday','Saturday'),
    ]

    semester   = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day        = models.CharField(max_length=15, choices=DAYS)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    room       = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.subject.name} - {self.day} {self.start_time}"

class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return f"{self.student.name} - {self.subject}"