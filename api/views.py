from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated

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



def set_jwt_cookie(response, access_token, refresh_token=None):
    response.set_cookie('access_token', access_token, httponly=True)
    
    if refresh_token:
        response.set_cookie('refresh_token', refresh_token, httponly=True)
    
    return response

@login_required
def issue_jwt_token(request):
    print("ran issue_jwt_token")
    print("request.user",request.user)
    user = request.user  # The authenticated user
    refresh = RefreshToken.for_user(user)  


    response = JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

    set_jwt_cookie(response, str(refresh.access_token), str(refresh))

    #print("response", response)
    #return response
    return redirect('/')



@api_view(['POST'])
def custom_refresh_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#from django.contrib.auth.views import LogoutView

def custom_logout(request):
    # Clear the session using Django's default session-based authentication
    logout(request)  # Logs out the user by clearing the session

    response = JsonResponse({"message": "Logged out successfully"})
    
    response.delete_cookie('access_token')

    response.delete_cookie('refresh_token')

    return redirect('/') 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Protected endpoint that requires authentication.
    """
    print("message:"+ "You have accessed a protected endpoint"+ "user"+ request.user.username)
    return JsonResponse({"message": "You have accessed a protected endpoint", "user": request.user.username})


