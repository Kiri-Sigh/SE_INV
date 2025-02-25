from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import LockerSet, ItemInOneLocker, Locker, RelItemInOneLocker, LockerInteractionLog
from user.models import CustomUser
from session.models import CheapItemSessionData, ExpensiveItemSessionData, Session
from inventory.models import ComponentCategory, CheapItem, ExpensiveItem
import uuid

class LockerSetTests(TestCase):
    def setUp(self):
        self.locker_set = LockerSet.objects.create(
            locker_set_dimensions_x=5,
            locker_set_dimensions_y=4,
            available=True,
            location="Building A",
            locker_colors="Blue"
        )

    def test_locker_set_creation(self):
        self.assertEqual(self.locker_set.locker_set_dimensions_x, 5)
        self.assertEqual(self.locker_set.locker_set_dimensions_y, 4)
        self.assertTrue(self.locker_set.available)
        self.assertEqual(self.locker_set.location, "Building A")
        self.assertEqual(self.locker_set.locker_colors, "Blue")
        self.assertIsInstance(self.locker_set.locker_set_id, uuid.UUID)

class ItemInOneLockerTests(TestCase):
    def setUp(self):
        self.item_in_locker = ItemInOneLocker.objects.create()

    def test_item_in_locker_creation(self):
        self.assertIsInstance(self.item_in_locker.item_in_one_locker_id, uuid.UUID)

class LockerTests(TestCase):
    def setUp(self):
        self.locker_set = LockerSet.objects.create(
            locker_set_dimensions_x=5,
            locker_set_dimensions_y=4,
            location="Building A"
        )

    def test_locker_creation(self):
        locker = Locker.objects.create(
            locker_position_x=2,
            locker_position_y=3,
            locker_set=self.locker_set,
            condition="Good condition"
        )
        self.assertEqual(locker.locker_position_x, 2)
        self.assertEqual(locker.locker_position_y, 3)
        self.assertEqual(locker.locker_set, self.locker_set)
        self.assertEqual(locker.condition, "Good condition")
        self.assertIsInstance(locker.locker_id, uuid.UUID)

# class RelItemInOneLockerTests(TestCase):
#     def setUp(self):
#         # Create necessary related objects
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
        
#         self.cheap_session = CheapItemSessionData.objects.create(
#             cheap=self.cheap_item,
#             session=self.session,
#             quantity=1,
#             date_start=timezone.now(),
#             date_end=timezone.now() + timedelta(days=7),
#             cheapItemSessionData_comment="Test comment",
#             cheapItemSessionData_status='P'
#         )
        
#         self.expensive_session = ExpensiveItemSessionData.objects.create(
#             expensive=self.cheap_item,
#             session=self.session,
#             quantity=1,
#             date_start=timezone.now(),
#             date_end=timezone.now() + timedelta(days=7),
#             cheapItemSessionData_comment="Test comment",
#             cheapItemSessionData_status='P'
#         )
        
#         self.item_in_locker = ItemInOneLocker.objects.create()
        
#         self.rel_item = RelItemInOneLocker.objects.create(
#             item_in_one_locker=self.item_in_locker,
#             expensive_session=self.expensive_session,
#             cheap_session=self.cheap_session
#         )

#     def test_rel_item_creation(self):
#         self.assertEqual(self.rel_item.item_in_one_locker, self.item_in_locker)
#         self.assertEqual(self.rel_item.expensive_session, self.expensive_session)
#         self.assertEqual(self.rel_item.cheap_session, self.cheap_session)
#         self.assertIsInstance(self.rel_item.rel_item_in_one_locker_id, uuid.UUID)

class LockerInteractionLogTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.locker_set = LockerSet.objects.create(
            locker_set_dimensions_x=5,
            locker_set_dimensions_y=4,
            location="Building A"
        )

    # def test_interaction_log_creation(self):
    #     locker = Locker.objects.create(
    #         locker_position_x=2,
    #         locker_position_y=3,
    #         locker_set=self.locker_set,
    #         condition="Good condition"
    #     )
    #     item_in_locker = ItemInOneLocker.objects.create()
    #     current_time = timezone.now()
        
    #     interaction_log = LockerInteractionLog.objects.create(
    #         name="Test User",
    #         locker=locker,
    #         start_date_pos=current_time,
    #         end_date_pos=current_time + timedelta(hours=1),
    #         user=self.user,
    #         date_time_interaction=current_time,
    #         operation='G',  # Get Item
    #         itemInOneLocker=item_in_locker
    #     )
        
    #     self.assertEqual(interaction_log.name, "Test User")
    #     self.assertEqual(interaction_log.locker, locker)
    #     self.assertEqual(interaction_log.start_date_pos, current_time)
    #     self.assertEqual(interaction_log.end_date_pos, current_time + timedelta(hours=1))
    #     self.assertEqual(interaction_log.user, self.user)
    #     self.assertEqual(interaction_log.date_time_interaction, current_time)
    #     self.assertEqual(interaction_log.operation, 'G')
    #     self.assertEqual(interaction_log.itemInOneLocker, item_in_locker)
    #     self.assertIsInstance(interaction_log.locker_log_id, uuid.UUID)
