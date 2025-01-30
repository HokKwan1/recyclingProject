# tests/test_forms.py
from django.test import TestCase
from portal.forms import LoginForm

class LoginFormTest(TestCase):

    def test_valid_form(self):
        # Test that the form is valid with correct data.
        form_data = {
            'user_name': 'testuser',
            'password': 'testpassword',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        # Test that the form is invalid when the username is missing.
        form_data = {
            'user_name': '',
            'password': 'testpassword',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user_name', form.errors)

    def test_invalid_form_missing_password(self):
        # Test that the form is invalid when the password is missing.
        form_data = {
            'user_name': 'testuser',
            'password': '',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_invalid_form_empty(self):
        # Test that the form is invalid when both fields are empty.
        form_data = {}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user_name', form.errors)
        self.assertIn('password', form.errors)
