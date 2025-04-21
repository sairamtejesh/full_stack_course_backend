from django.urls import path
from . import views

urlpatterns = [
    # Courses & Videos
    path('courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('videos/', views.VideoListAPIView.as_view(), name='video-list'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),

    # Wallet & Gamification
    path('wallet/', views.user_wallet, name='user-wallet'),
    path('complete-video/<int:video_id>/', views.complete_video, name='complete-video'),
    path('unlock-course/<int:course_id>/', views.unlock_course, name='unlock-course'),
]
