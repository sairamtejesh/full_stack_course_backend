from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Course

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        
        # Automatically unlock "SQL" course
        try:
            sql_course = Course.objects.get(title__icontains="sql")
            profile.unlocked_courses.add(sql_course)
        except Course.DoesNotExist:
            pass  # If SQL course not found, skip
