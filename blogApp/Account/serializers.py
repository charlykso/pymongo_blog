from .models import CustomUser, Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'password',
            'username',
            'role',
            'is_active',
            'is_staff',
            'created_at',
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return token


class AllUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'role',
            'is_active',
            'is_staff',
            'created_at',
            'updated_at',
            'groups',
            'profile',
        )

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'phone',
            'githubUsername',
            'profilePic',
            'updated_at',
        )
    
class UserSigninSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'role',
            'is_active',
            'created_at',
            'profile',
        )