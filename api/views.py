from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa

@api_view(['POST'])
@psa('social:complete')
def exchange_google_token(request):
    """ Exchange Google OAuth2 token for a JWT """
    token = request.data.get("access_token")  # Get the Google OAuth2 token from frontend

    if not token:
        return Response({"error": "Access token required"}, status=400)

    user = request.backend.do_auth(token)

    if user and user.is_active:
        refresh = RefreshToken.for_user(user)  # Generate JWT tokens
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

    return Response({"error": "Invalid credentials"}, status=400)


from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

def set_jwt_cookie(response, token):
    # Set the JWT token as an HTTP-only cookie for added security
    response.set_cookie('access_token', token, httponly=True)  # Set access token as a cookie
    return response


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@login_required
def issue_jwt_token(request):
    print("ran issue_jwt_token")
    user = request.user  # The authenticated user
    refresh = RefreshToken.for_user(user)  # Create a refresh and access token
    #print("refresh?:",refresh)
    # Use set_jwt_cookie to store the access token in the cookie
    response = JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

    # Store the access token in the HTTP-only cookie
    #print("refresh.access_token",refresh.access_token)
    #print("refresh.access_token",refresh.access_token)
    set_jwt_cookie(response, str(refresh.access_token))
    print("response",response)
    return response


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def custom_refresh_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode the refresh token and get the new access token
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
