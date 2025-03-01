# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from .models import AdminUser, StudentUser, UserKey, CustomUser
# from django.contrib.auth.models import User
# from django.test import override_settings
# import uuid

# # Create your tests here.

# class AdminUserTests(TestCase):
#     def setUp(self):
#         self.admin_user = AdminUser.objects.create(
#             name="Test Admin",
#             gmail="admin@test.com",
#             role='S'  # Super admin
#         )

#     def test_admin_user_creation(self):
#         self.assertEqual(self.admin_user.name, "Test Admin")
#         self.assertEqual(self.admin_user.gmail, "admin@test.com")
#         self.assertEqual(self.admin_user.role, 'S')
#         self.assertIsInstance(self.admin_user.user_id, uuid.UUID)

# class StudentUserTests(TestCase):
#     def setUp(self):
#         self.student_user = StudentUser.objects.create(
#             name="Test Student",
#             enrolled_year=2024,
#             enrolled_department="Computer Science",
#             merit=100,
#             level=3
#         )

#     def test_student_user_creation(self):
#         self.assertEqual(self.student_user.name, "Test Student")
#         self.assertEqual(self.student_user.enrolled_year, 2024)
#         self.assertEqual(self.student_user.enrolled_department, "Computer Science")
#         self.assertEqual(self.student_user.merit, 100)
#         self.assertEqual(self.student_user.level, 3)
#         self.assertIsInstance(self.student_user.user_id, uuid.UUID)

# class CustomUserTests(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="testpass123",
#             email="test@example.com",
#             enrolled_year=2024,
#             enrolled_department="Computer Science",
#             merit=100,
#             level=3,
#             google_id="test_google_id",
#             profile_picture="http://example.com/pic.jpg"
#         )

#     def test_custom_user_creation(self):
#         self.assertEqual(self.user.username, "testuser")
#         self.assertEqual(self.user.email, "test@example.com")
#         self.assertEqual(self.user.enrolled_year, 2024)
#         self.assertEqual(self.user.enrolled_department, "Computer Science")
#         self.assertEqual(self.user.merit, 100)
#         self.assertEqual(self.user.level, 3)
#         self.assertEqual(self.user.google_id, "test_google_id")
#         self.assertEqual(self.user.profile_picture, "http://example.com/pic.jpg")
#         self.assertTrue(self.user.check_password("testpass123"))

# class UserKeyTests(TestCase):
#     def setUp(self):
#         self.user_key = UserKey.objects.create(
#             student_id="CS2024001",
#             price=99.99,
#             description="Test key description",
#             status='P'  # Pending
#         )

#     def test_user_key_creation(self):
#         self.assertEqual(self.user_key.student_id, "CS2024001")
#         self.assertEqual(float(self.user_key.price), 99.99)
#         self.assertEqual(self.user_key.description, "Test key description")
#         self.assertEqual(self.user_key.status, 'P')
#         self.assertIsInstance(self.user_key.user_id, uuid.UUID)

# class ViewTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(
#             username="testuser",
#             password="testpass123",
#             email="test@example.com",
#             enrolled_year=2024,
#             enrolled_department="Computer Science"
#         )

#     def test_profile_view_authenticated(self):
#         self.client.login(username="testuser", password="testpass123")
#         response = self.client.get(reverse('user:profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'profile.html')

#     def test_profile_view_unauthenticated(self):
#         response = self.client.get(reverse('user:profile'))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, '/login/')

#     @override_settings(SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='test_key', 
#                       SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='test_secret')
#     def test_social_profile_view(self):
#         self.client.login(username="testuser", password="testpass123")
#         response = self.client.get(reverse('user:social_profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/social_profile.html')
