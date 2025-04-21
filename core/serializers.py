from rest_framework import serializers
from .models import Course, Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'order', 'uploaded_at']

class CourseSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'created_at', 'videos']
