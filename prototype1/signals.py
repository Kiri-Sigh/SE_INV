# from django.dispatch import receiver
# from social_django.signals import social_auth_registered
# from user.models import CustomUser

# @receiver(social_auth_registered)
# def create_user_profile(sender, request, sociallogin, **kwargs):
#     user = sociallogin.user
#     user.google_id = sociallogin.uid
#     user.profile_picture = sociallogin.extra_data.get('picture', '')
#     user.save()
