from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Profile
from .serializers import UserSerializer, ProfileSerializer, CreateUserSerializer
from pymongo.collection import Collection
from django.contrib.auth.hashers import make_password

# Create your views here.
@api_view(['GET'])
def status(request):
    return Response({'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create(request):
    try:
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            # hashing password before saving
            # get the password from the serializer
            password = serializer.validated_data['password']
            newpassword = make_password(password)
            # get an instance of the user
            user = CustomUser(
                username=serializer.validated_data['username'], email=serializer.validated_data['email'], password=newpassword)
            serializer.validated_data['password'] = user.password
            serializer.validated_data['is_active'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def allUsers(request):
    try:
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUser(request, id):
    try:
        user = CustomUser.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

