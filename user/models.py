from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# class AdminUser(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     gmail = models.EmailField()
#     STATUS_CHOICES = [('S', 'Super'), ('N', 'Normal')]
#     role = models.CharField(max_length=1, choices=STATUS_CHOICES)

#     def __str__(self):
#         return self.name


# class StudentUser(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     enrolled_year = models.IntegerField()
#     enrolled_department = models.CharField(max_length=100)
#     merit = models.IntegerField()
#     level = models.IntegerField()

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser):
#     google_id = models.CharField(max_length=100, blank=True, null=True)
#     profile_picture = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.username

class CustomUser(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    # ROLE_CHOICES = [
    #     ("user", "User"),
    #     ("manager", "Manager"),
    #     ("admin", "Admin"),
    # ]
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    enrolled_year = models.IntegerField(default=2024)
    enrolled_department = models.CharField(
        max_length=100, blank=True, default="")
    merit = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    # image = CloudinaryField('image',blank=True, null=True)

    def __str__(self):
        return self.username
# class UserKey(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     student_id = models.CharField(max_length=10)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)

#     def __str__(self):
#         return self.name
