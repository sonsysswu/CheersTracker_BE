from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class JoinView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 사용자가 인증되었는지 확인
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 사용자 인증 성공 시 토큰 생성 및 반환
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data  # 사용자 데이터를 직렬화
            return Response({'token': token.key, 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)