from django.test import TestCase
from django.contrib.auth.models import User
from homepage.models import Request
from datetime import datetime
from django.utils.timezone import make_aware

class RequestModelTest(TestCase):
    def setUp(self):
        # Set up test data before each test
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.request = Request.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address="123 Street",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10001",
            status="pending",
            date_created=make_aware(datetime(2024, 1, 1, 12, 0, 0)),
            token="abcd1234",
            claimed_by=self.user
        )

    def test_request_creation(self):
        # Test if the Request object is created correctly
        self.assertEqual(self.request.first_name, "John")
        self.assertEqual(self.request.last_name, "Doe")
        self.assertEqual(self.request.email, "john.doe@example.com")
        self.assertEqual(self.request.phone, "1234567890")
        self.assertEqual(self.request.status, "pending")
        self.assertEqual(self.request.claimed_by.username, "testuser")
        self.assertIsNotNone(self.request.token)

    def test_string_representation(self):
        # Test if __str__ returns the expected output
        self.assertEqual(str(self.request), "John Doe")

    def test_status_choices(self):
        # Ensure the status choices are valid
        self.request.status = "in_progress"
        self.request.save()
        self.assertEqual(self.request.status, "in_progress")

        self.request.status = "completed"
        self.request.save()
        self.assertEqual(self.request.status, "completed")

    def test_date_completed_can_be_null(self):
        # Ensure date_completed can be null
        self.assertIsNone(self.request.date_completed)

