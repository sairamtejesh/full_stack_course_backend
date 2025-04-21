from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    coin_price = models.IntegerField(default=25)  # Add coin price
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    order = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    completed_videos = models.ManyToManyField(Video, blank=True)
    unlocked_courses = models.ManyToManyField(Course, blank=True)  # This is okay now

    def __str__(self):
        return self.user.username
