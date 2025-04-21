from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Course, Video, UserProfile
from .serializers import CourseSerializer, VideoSerializer

# -------------------------------
# Course & Video API Views
# -------------------------------

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# -------------------------------
# Auth APIs: Signup & Login
# -------------------------------

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'username': user.username})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})

# -------------------------------
# Wallet API (for Coins, Unlocks, Progress)
# -------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_wallet(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return Response({
        'coins': profile.coins,
        'completed_videos': [v.id for v in profile.completed_videos.all()],
        'unlocked_courses': [c.id for c in profile.unlocked_courses.all()]
    })

# -------------------------------
# Complete Video API (Rewards 5 coins)
# -------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_video(request, video_id):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=404)

    if profile.completed_videos.filter(id=video_id).exists():
        return Response({'message': 'Video already completed', 'coins': profile.coins})

    profile.completed_videos.add(video)
    profile.coins += 5
    profile.save()

    return Response({
        'message': 'Video completed and coins rewarded',
        'coins': profile.coins
    })

# -------------------------------
# Unlock Course API (Uses dynamic coin_price)
# -------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_course(request, course_id):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

    if profile.unlocked_courses.filter(id=course_id).exists():
        return Response({'message': 'Course already unlocked', 'coins': profile.coins})

    try:
        cost = int(course.coin_price)
    except (TypeError, ValueError):
        cost = 25

    if profile.coins < cost:
        return Response({'error': f'Not enough coins. Requires {cost} coins.'}, status=400)

    profile.coins -= cost
    profile.unlocked_courses.add(course)
    profile.save()

    return Response({
        'message': f'{course.title} unlocked successfully',
        'coins': profile.coins
    })

# -------------------------------
# Temporary Debug Endpoint
# -------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def check_users(request):
    try:
        count = User.objects.count()
        return Response({'users': count})
    except Exception as e:
        return Response({'error': str(e)})
