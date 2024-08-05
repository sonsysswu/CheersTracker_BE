from rest_framework import serializers
from .models import Post, Comment
from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        # 현재 사용자 정보를 가져와서 author 필드에 추가
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

