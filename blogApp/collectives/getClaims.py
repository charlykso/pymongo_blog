from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

def get_claims_from_simplejwt_token(request):
    user, token = JWTAuthentication().authenticate(request)[:2]
    return {
        'user': user,
        'token': token,
    }