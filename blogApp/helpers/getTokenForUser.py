from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from Account.serializers import AllUserSerializer
from Account.models import CustomUser

def get_token_for_user(newuser):
    user = CustomUser.objects.get(id=newuser['id'])
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    user = AllUserSerializer(user, many=False)
    user_details = {
            'id': user.data['id'],
            'role': user.data['role'],
            'username': user.data['username'],
            'email': user.data['email'],
            'is_active': user.data['is_active'],
            'is_staff': user.data['is_staff'],
            'created_at': user.data['created_at'],
            'profile': user.data['profile']
        }
    return {
        'user': user_details,
        'token': {
            'access': access_token,
            'refresh': str(refresh)
        }
    }