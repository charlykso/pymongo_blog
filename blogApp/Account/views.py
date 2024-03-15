from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Profile
from .serializers import UserSerializer, ProfileSerializer, CreateUserSerializer, MyTokenObtainPairSerializer, AllUserSerializer, UpdateProfileSerializer
from pymongo.collection import Collection
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpRequest
from collectives.getClaims import get_claims_from_simplejwt_token
from django.contrib.auth.models import Group
from django.db.models import Prefetch

# Create your views here.


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_status(request):
    return Response('API is running', status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            request = HttpRequest()
            request.META['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(response.data['access'])
            user = get_claims_from_simplejwt_token(request)
            _object = user
            _id = _object['user'].id
            # use the id to get the new user
            new_user  = CustomUser.objects.get(id=_id)
            serializer = UserSerializer(new_user, many=False)
            # create a new response object
            new_response = Response()
            new_response.data = {
                'user': serializer.data,
                'token': response.data
            }
            # return the new response object
            return new_response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes((AllowAny,))
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
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            group = Group.objects.get(name='User')
            user.groups.add(group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        if str(e) == "":
            return Response({'error': 'User with that email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def allUsers(request):
    try:
        users = CustomUser.objects.all().order_by('-created_at').prefetch_related(Prefetch('profile', queryset=Profile.objects.all()))
        serializer = AllUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def getUser(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def updateUser(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteUser(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
        user.delete()
        return Response('User deleted', status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_profiles(request):
    try:
        profile = Profile.objects.all().order_by('-created_at')
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_user_profile(request, pk):
    try:
        profile = Profile.objects.get(user=pk)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def updateProfile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        serializer = UpdateProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
