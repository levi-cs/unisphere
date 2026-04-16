from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student


@receiver(pre_save, sender=Student)
def create_user_for_student(sender, instance, **kwargs):
    if not instance.user:
        email = instance.email

        user = User.objects.filter(username=email).first()

        if not user:
            user = User.objects.create_user(
                username=email,
                email=email,
                password="student123"
            )

        instance.user = user