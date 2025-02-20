from user.models import CustomUser
#kwargs social and req is nothing
#kwargs social return str before @ of email
#kwargs req is just the endp of the req of login 

#pipeline returns dict to next pipline and it will be in kwargs dict
def set_student_defaults(strategy, details, backend, user=None, *args, **kwargs):
    """ Ensure new users have required fields """
    print("-----------set_student_defaults----------")

    if user and isinstance(user, CustomUser):  # Check if user exists & is correct type
        user.enrolled_year = 2024
        user.merit = 0
        user.save()
    return {'user': user}
# def save_google_profile(backend, user, response, *args, **kwargs):
#     """
#     Save additional data from Google's API to the user profile.
#     """
#     if backend.name == "google-oauth2":
#         if user.social_auth.filter(provider=backend.name).exists():
#             user.google_id = response.get("sub")  # Save Google ID
#             user.profile_picture = response.get("picture")  # Save profile picture
#             user.save()
#         else:
#             # Optionally create a profile if one doesn't exist
#             user.google_id = response.get("sub")  # Save Google ID
#             user.profile_picture = response.get("picture")  # Save profile picture
#             user.save()

# user/pipeline.py

from social_django.models import UserSocialAuth

#successfully created ;-;
def save_google_profile2(backend, user, response, *args, **kwargs):
    print("-----------save_google_profile----------")
    
    if backend.name == 'google-oauth2':
        email = response.get('email')  # Google's unique user ID
        profile_picture = response.get('picture', None)
        google_uid = response.get('sub')  # Google's unique user ID

        #custom_user = CustomUser.objects.filter(email=email).first()
        print("profile pic",profile_picture)
        #custom_user.profile_picture = profile_picture
        #custom_user.save()
        # Ensure the user exists in UserSocialAuth
        custom_user = CustomUser.objects.filter( google_id=google_uid).first()

        if custom_user:
            print("create custom user")
            custom_user.profile_picture = profile_picture
            custom_user.save()
        else:
            print("another_email:",CustomUser.objects.filter( email=email).first().email)
            print("true?:",CustomUser.objects.filter( email=email).first().email=="syril.tuladhar.2@gmail.com")
            
            another_user=CustomUser.objects.filter( email=email).first()
        
            another_user.profile_picture = profile_picture
            another_user.google_id = google_uid
            another_user.save()
            print("saving...")
            # if not custom_user:
            #     # Create a new CustomUser if not found
            #     custom_user = CustomUser.objects.create(
            #         google_id=google_uid,
            #         email=email,
            #         profile_picture=profile_picture
            #     )
            # else:
            #     # Update the existing user’s profile picture
            #     custom_user.profile_picture = profile_picture
            #     custom_user.google_id = google_uid
            #     custom_user.save()
            
            print(f"Custom user created: {custom_user is not None}")
            #print(f"Profile picture URL: {custom_user.profile_picture}")
        
            #print("User not found in UserSocialAuth")

def save_google_profile(backend, user, response, *args, **kwargs):
    print("-----------save_google_profile----------")
    
    if backend.name == 'google-oauth2':
        email = response.get('email')  # Google's unique user ID
        profile_picture = response.get('picture', None)
        google_uid = response.get('sub')  # Google's unique user ID

        print("profile pic", profile_picture)
        
        # Ensure the user exists in UserSocialAuth
        custom_user = CustomUser.objects.filter(google_id=google_uid).first()

        if custom_user:
            print("Updating existing user")
            custom_user.profile_picture = profile_picture
            custom_user.save()
            print("User updated:", custom_user)
        else:
            print(f"Checking for user with email: {email}")
            another_user = CustomUser.objects.filter(email=email).first()

            if another_user:
                print("User found with email:", another_user.email)
                another_user.profile_picture = profile_picture
                another_user.google_id = google_uid
                try:
                    another_user.save()
                    print("User saved:", another_user)
                except Exception as e:
                    print(f"Error saving user: {e}")
            else:
                print("No user found with the email, creating a new user.")
                try:
                    custom_user = CustomUser.objects.create(
                        google_id=google_uid,
                        email=email,
                        profile_picture=profile_picture
                    )
                    print("New user created:", custom_user)
                except Exception as e:
                    print(f"Error creating user: {e}")

def save_google_session(backend, user, response, request, *args, **kwargs):
    if backend.name == "google-oauth2":
        #print("running save_google_session")
        request.session["google_id"] = response.get("sub")  # Store Google ID


from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated
from social_django.models import UserSocialAuth

User = get_user_model()

#useless
def allow_reassociation(backend, user, *args, **kwargs):
    #print("--------ALLOW_REASSOCIATION--------")
    
    if not user:
        email = kwargs.get('details', {}).get('email')
        if email:
            try:
                # Find existing user by email
                user = get_user_model().objects.get(email=email)
                existing_social_user = UserSocialAuth.objects.filter(user=user, provider=backend.name).exists()
                if existing_social_user:
                    return {'user': user}
                else:
                    raise AuthAlreadyAssociated(backend)
            except get_user_model().DoesNotExist:
                pass
    return None

#useless
def auto_login_existing_user(backend, uid, user=None, response=None, *args, **kwargs):
    print("--------auto_login_existing_user--------")

    """
    If a user tries to log in with a social account that already exists, log them in.
    """
    if user:  # User is already authenticated, no need to check
        return {"user": user}

    social_auth = UserSocialAuth.objects.filter(provider=backend.name, uid=uid).first()
    #print("social_auth: ",social_auth)
    if social_auth:
        return {"user": social_auth.user}  # Log in the existing user

    # If no social auth exists, check if there's a user with the same email
    email = kwargs.get("details", {}).get("email")
    if email:
        try:

            existing_user = User.objects.get(email=email)
            #print("existing_user: ",existing_user)
            return {"user": existing_user}  # Log in the user with the existing email
        except User.DoesNotExist:
            pass

    return None  # Continue with default pipeline (creating new user if necessary)


from social_core.exceptions import AuthException

def print_google_response(backend, user,strategy, response,uid,details, *args, **kwargs):
   # print("jwtauth",JWTAuthentication())
    print("Current strategy:", strategy)
    print("request",request)
    print("backend",backend)
    print("Current user:", user)
    print("Current details:", details)
    print("Current uid:", uid)
    print("Current uid:", uid)   
    print("Current *args", args)
    #print("Current *args", *args)
    print("Current  **kwargs", kwargs)
    request = kwargs.get('social')
    print("kwargs - social: ", request)
    print("")
    print("picture?:",response.get('picture', None))
    """
    This function prints the response data received from Google
    when a user logs in via Google OAuth2.
    """
    if backend.name == 'google-oauth2':  # Ensure it's Google OAuth2
        print("========== GOOGLE ACCOUNT DATA ==========")
        print(response)  # Print full response from Google
        print("=========================================")

    return None
