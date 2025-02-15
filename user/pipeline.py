from user.models import CustomUser

def set_student_defaults(strategy, details, backend, user=None, *args, **kwargs):
    """ Ensure new users have required fields """
    if user and isinstance(user, CustomUser):  # Check if user exists & is correct type
        user.enrolled_year = 2024
        user.merit = 0
        user.save()
    return {'user': user}
def save_google_profile(backend, user, response, *args, **kwargs):
    """
    Save additional data from Google's API to the user profile.
    """
    if backend.name == "google-oauth2":
        user.profile.picture = response.get("picture")
        user.profile.save()
