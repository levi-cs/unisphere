"""
UniSphere — One-Click Setup Script
Run this ONCE after installing requirements:
    python setup.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unisphere.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run migrations first
os.system(f'{sys.executable} manage.py makemigrations')
os.system(f'{sys.executable} manage.py migrate')
os.system(f'{sys.executable} manage.py collectstatic --noinput')

django.setup()

from django.contrib.auth.models import User
from main.models import (Course, Semester, Student, Teacher, Subject,
                         Attendance, Material, Notice, Announcement, Timetable)

print("\n🎓 UniSphere Setup — Creating demo data...\n")

# ── Courses ──────────────────────────────────────────
cse,  _ = Course.objects.get_or_create(name='B.Tech Computer Science & Engineering')
ece,  _ = Course.objects.get_or_create(name='B.Tech Electronics & Communication')
mba,  _ = Course.objects.get_or_create(name='MBA Business Administration')
print("✅ Courses created")

# ── Semesters ─────────────────────────────────────────
sems = {}
for n in range(1, 9):
    s, _ = Semester.objects.get_or_create(number=n)
    sems[n] = s
print("✅ Semesters created")

# ── Admin ─────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@unisphere.edu', 'admin123')
    print("✅ Admin created  →  username: admin  |  password: admin123")

# ── Teachers ──────────────────────────────────────────
def make_teacher(username, email, password, name, tid, dept, phone=''):
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password, first_name=name.split()[0])
        Teacher.objects.create(user=u, name=name, teacher_id=tid, email=email, department=dept, phone=phone)
        print(f"   Teacher: {name}  |  ID: {tid}  |  Pass: {password}")
        return Teacher.objects.get(teacher_id=tid)
    return Teacher.objects.get(teacher_id=tid)

print("\n✅ Teachers:")
t1 = make_teacher('rajan.mehta',  'rajan@unisphere.edu',  'teacher123', 'Dr. Rajan Mehta',  'TCH001', 'Computer Science', '9876543210')
t2 = make_teacher('sunita.rao',   'sunita@unisphere.edu', 'teacher456', 'Prof. Sunita Rao', 'TCH002', 'Computer Science', '9876543211')
t3 = make_teacher('arjun.pillai', 'arjun@unisphere.edu',  'teacher789', 'Dr. Arjun Pillai', 'TCH003', 'Computer Science', '9876543212')

# ── Subjects ──────────────────────────────────────────
def make_subject(name, code, credits, sem_num, teacher):
    s, _ = Subject.objects.get_or_create(
        code=code,
        defaults=dict(name=name, credits=credits, semester=sems[sem_num], teacher=teacher)
    )
    return s

dsa  = make_subject('Data Structures & Algorithms', 'CS301', 4, 3, t1)
os_  = make_subject('Operating Systems',            'CS302', 4, 3, t2)
dbms = make_subject('Database Management Systems',  'CS303', 3, 3, t3)
cn   = make_subject('Computer Networks',            'CS304', 4, 3, t2)
dm   = make_subject('Discrete Mathematics',         'MA301', 3, 3, t1)
se   = make_subject('Software Engineering',         'CS305', 3, 3, t3)
print("✅ Subjects created")

# ── Students ──────────────────────────────────────────
def make_student(username, email, password, name, sid, course, sem_num, phone=''):
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password, first_name=name.split()[0])
        s = Student.objects.create(user=u, name=name, student_id=sid, email=email,
                                   course=course, semester=sems[sem_num], phone=phone)
        print(f"   Student: {name}  |  ID: {sid}  |  Pass: {password}")
        return s
    return Student.objects.get(student_id=sid)

print("\n✅ Students:")
s1 = make_student('u18cs001', 'alex@unisphere.edu',   'student123', 'Alex Johnson',  'U18CS001', cse, 3, '9900000001')
s2 = make_student('u18cs002', 'priya@unisphere.edu',  'student456', 'Priya Sharma',  'U18CS002', cse, 3, '9900000002')
s3 = make_student('u18cs003', 'rahul@unisphere.edu',  'student789', 'Rahul Verma',   'U18CS003', cse, 3, '9900000003')

# ── Attendance ────────────────────────────────────────
att_data = [
    (s1, dsa,  46, 43), (s1, os_,  45, 35), (s1, dbms, 40, 27),
    (s1, cn,   46, 40), (s1, dm,   38, 32), (s1, se,   42, 34),
    (s2, dsa,  46, 40), (s2, os_,  45, 38), (s2, dbms, 40, 36),
    (s2, cn,   46, 42), (s2, dm,   38, 35), (s2, se,   42, 39),
]
for stu, sub, total, att in att_data:
    Attendance.objects.get_or_create(student=stu, subject=sub,
                                     defaults=dict(total_classes=total, attended=att))
print("✅ Attendance records created")

# ── Notices ───────────────────────────────────────────
notices = [
    ('Mid-Semester Examination Schedule — April 2026',
     'The mid-semester exams will be held from April 14–20, 2026. Detailed timetable attached via email.',
     'urgent', 'Academic Office'),
    ('Library Closure — Annual Stock Verification',
     'The central library will be closed on April 5–6, 2026 for annual stock verification.',
     'important', 'Library Department'),
    ('Sports Week Registration Open — April 8–12',
     'Students can register for various sports events through the Student Affairs portal.',
     'normal', 'Student Affairs'),
    ('Fee Payment Deadline — April 15, 2026',
     'Last date for payment of semester fees is April 15, 2026. Late fine will apply.',
     'important', 'Accounts Section'),
    ('National Scholarship Portal — Application Window',
     'Applications for national scholarships are open till April 30, 2026.',
     'normal', 'Scholarship Cell'),
]
for title, content, priority, posted_by in notices:
    Notice.objects.get_or_create(title=title,
                                  defaults=dict(content=content, priority=priority, posted_by=posted_by))
print("✅ Notices created")

# ── Announcements ─────────────────────────────────────
anns = [
    ('Guest Lecture: AI & Machine Learning in Industry', 'A guest lecture by industry experts on AI trends. Venue: Seminar Hall A, 3:00 PM today.', t1),
    ('DSA Internal Assessment — Rescheduled', 'The DSA internal assessment has been rescheduled to April 12, 2026.', t1),
    ('Hackathon 2026 — Team Registration Deadline April 8', 'Register your team for the annual hackathon. Max 4 members per team.', t2),
]
for title, content, teacher in anns:
    Announcement.objects.get_or_create(title=title, defaults=dict(content=content, teacher=teacher))
print("✅ Announcements created")

# ── Timetable ─────────────────────────────────────────
import datetime
tt_data = [
    (sems[3], dsa,  'Monday',    '09:00', '10:00', 'R101'),
    (sems[3], os_,  'Monday',    '10:00', '11:00', 'R202'),
    (sems[3], dbms, 'Monday',    '11:15', '12:15', 'L101'),
    (sems[3], os_,  'Tuesday',   '09:00', '10:00', 'R202'),
    (sems[3], dm,   'Tuesday',   '10:00', '11:00', 'R103'),
    (sems[3], cn,   'Tuesday',   '11:15', '12:15', 'R301'),
    (sems[3], dbms, 'Wednesday', '09:00', '10:00', 'L101'),
    (sems[3], dsa,  'Wednesday', '10:00', '11:00', 'Lab1'),
    (sems[3], dm,   'Wednesday', '11:15', '12:15', 'R103'),
    (sems[3], cn,   'Thursday',  '09:00', '10:00', 'R301'),
    (sems[3], dsa,  'Thursday',  '11:15', '12:15', 'R101'),
    (sems[3], dm,   'Thursday',  '13:00', '14:00', 'R103'),
    (sems[3], se,   'Friday',    '09:00', '10:00', 'R105'),
    (sems[3], dbms, 'Friday',    '10:00', '11:00', 'L101'),
    (sems[3], os_,  'Friday',    '11:15', '12:15', 'R202'),
    (sems[3], dsa,  'Friday',    '13:00', '14:00', 'R101'),
]
for sem, sub, day, start, end, room in tt_data:
    start_t = datetime.time(*map(int, start.split(':')))
    end_t   = datetime.time(*map(int, end.split(':')))
    Timetable.objects.get_or_create(
        semester=sem, subject=sub, day=day, start_time=start_t,
        defaults=dict(end_time=end_t, room=room)
    )
print("✅ Timetable created")

print("""
╔══════════════════════════════════════════════════════════╗
║           🎓  UniSphere Setup Complete!                  ║
╠══════════════════════════════════════════════════════════╣
║  Run the server:                                         ║
║     python manage.py runserver                           ║
║                                                          ║
║  Open:  http://127.0.0.1:8000                            ║
║                                                          ║
║  Login Credentials:                                      ║
║  ─────────────────────────────────────────────────────   ║
║  👨‍💼 Admin    : admin       / admin123                    ║
║  📖 Teacher  : TCH001      / teacher123                  ║
║  🎒 Student  : U18CS001    / student123                  ║
║  🎒 Student  : U18CS002    / student456                  ║
╚══════════════════════════════════════════════════════════╝
""")
