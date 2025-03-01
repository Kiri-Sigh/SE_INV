# from django.test import TestCase
# from django.utils import timezone
# from datetime import timedelta
# from .models import Session, CheapItemSessionData, ExpensiveItemSessionData, CompletedRecord
# from inventory.models import CheapItem, ExpensiveItem, ComponentCategory
# from user.models import CustomUser
# from locker.models import Locker, LockerSet
# import uuid

# class SessionTests(TestCase):
#     def setUp(self):
#         # Create necessary related objects
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Test Item",
#             category=self.category,
#             stock=5,
#             description="Test description",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )
        
#         self.session = Session.objects.create(
#             name="Test Session",
#             price=99.99,
#             description="Test session description",
#             author=self.expensive_item,
#             status='P'  # Pending
#         )

#     def test_session_creation(self):
#         self.assertEqual(self.session.name, "Test Session")
#         self.assertEqual(float(self.session.price), 99.99)
#         self.assertEqual(self.session.description, "Test session description")
#         self.assertEqual(self.session.author, self.expensive_item)
#         self.assertEqual(self.session.status, 'P')
#         self.assertIsInstance(self.session.user_id, uuid.UUID)

# class CheapItemSessionDataTests(TestCase):
#     def setUp(self):
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.cheap_item = CheapItem.objects.create(
#             name="Test Cheap Item",
#             category=self.category,
#             stock=100,
#             description="Test description",
#             quantity_available=90,
#             quantity_borrowed=10,
#             weight=1,
#             amount_reserve=20,
#             percent_reserve=20
#         )
        
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Test Item",
#             category=self.category,
#             stock=5,
#             description="Test description",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )
        
#         self.session = Session.objects.create(
#             name="Test Session",
#             price=99.99,
#             description="Test session description",
#             author=self.expensive_item,
#             status='P'
#         )

#     # def test_cheap_session_data_creation(self):
#     #     cheap_session_data = CheapItemSessionData.objects.create(
#     #         cheap=self.cheap_item,
#     #         session=self.session,
#     #         quantity=5,
#     #         date_start=timezone.now(),
#     #         date_end=timezone.now() + timedelta(days=7),
#     #         cheapItemSessionData_comment="Test comment",
#     #         cheapItemSessionData_status='P'
#     #     )
#     #     self.assertEqual(cheap_session_data.cheap, self.cheap_item)
#     #     self.assertEqual(cheap_session_data.session, self.session)
#     #     self.assertEqual(cheap_session_data.quantity, 5)
#     #     self.assertEqual(cheap_session_data.cheapItemSessionData_comment, "Test comment")
#     #     self.assertEqual(cheap_session_data.cheapItemSessionData_status, 'P')

# class ExpensiveItemSessionDataTests(TestCase):
#     def setUp(self):
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Test Item",
#             category=self.category,
#             stock=5,
#             description="Test description",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )
        
#         self.session = Session.objects.create(
#             name="Test Session",
#             price=99.99,
#             description="Test session description",
#             author=self.expensive_item,
#             status='P'
#         )

#     # def test_expensive_session_data_creation(self):
#     #     expensive_session_data = ExpensiveItemSessionData.objects.create(
#     #         expensive=self.expensive_item,
#     #         session=self.session,
#     #         quantity=1,
#     #         date_start=timezone.now(),
#     #         date_end=timezone.now() + timedelta(days=7),
#     #         cheapItemSessionData_comment="Test comment",
#     #         cheapItemSessionData_status='P'
#     #     )
#     #     self.assertEqual(expensive_session_data.expensive, self.expensive_item)
#     #     self.assertEqual(expensive_session_data.session, self.session)
#     #     self.assertEqual(expensive_session_data.quantity, 1)
#     #     self.assertEqual(expensive_session_data.cheapItemSessionData_comment, "Test comment")
#     #     self.assertEqual(expensive_session_data.cheapItemSessionData_status, 'P')

# class CompletedRecordTests(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             username="testuser",
#             password="testpass123",
#             email="test@example.com",
#             enrolled_year=2024,
#             enrolled_department="Computer Science"
#         )

#     # def test_completed_record_creation(self):
#     #     completed_record = CompletedRecord.objects.create(
#     #         user=self.user,
#     #         admin_user=self.user,  # Using same user as admin for testing
#     #         session_date_posted=timezone.now(),
#     #         record_date_posted=timezone.now(),
#     #         condition="Good condition",
#     #         session_user_comment="User comment",
#     #         session_admin_comment="Admin comment",
#     #         session_status_final='C'  # Completed
#     #     )
#     #     self.assertEqual(completed_record.user, self.user)
#     #     self.assertEqual(completed_record.admin_user, self.user)
#     #     self.assertEqual(completed_record.condition, "Good condition")
#     #     self.assertEqual(completed_record.session_user_comment, "User comment")
#     #     self.assertEqual(completed_record.session_admin_comment, "Admin comment")
#     #     self.assertEqual(completed_record.session_status_final, 'C')
#     #     self.assertIsInstance(completed_record.record_id, uuid.UUID)
