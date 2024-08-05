from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ChangePasswordSerializer, EncryptedUserSerializer
from .models import CustomUser

User = get_user_model()

# 회원가입 로직
class JoinView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 로그인 로직
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            return Response({'token': token.key, 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 변경 로직
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 사용자 정보 조회 (현재 사용자 정보)
class EncryptedUserView(generics.RetrieveAPIView):
    serializer_class = EncryptedUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# 전체 사용자 목록 조회 (관리자용)
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# 현재 사용자 상세 정보 조회
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
