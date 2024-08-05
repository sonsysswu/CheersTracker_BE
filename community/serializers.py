from rest_framework import serializers
from .models import Post, Comment
from user.serializers import UserSerializer  # 사용자 정보를 직렬화하기 위한 serializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # 글 작성자 정보 포함

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        # 요청 정보를 통해 현재 사용자 정보를 가져와서 author 필드에 추가
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # 댓글 작성자 정보 포함

    class Meta:
        model = Comment
        fields = '__all__'
