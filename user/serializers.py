from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import encrypt_message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'birthdate', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class EncryptedUserSerializer(serializers.ModelSerializer):
    encrypted_username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['encrypted_username']

    def get_encrypted_username(self, obj):
        return encrypt_message(obj.username)
