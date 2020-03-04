from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):
    """Test for managing the user model"""

    def test_create_user(self):
        """Test if regular user can be successfully created"""
        User = get_user_model()
        user = User.objects.create_user(
            email='test@user.com',
            first_name='jerry',
            last_name='test',
            password='123'
        )
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                first_name='jerry',
                last_name='test',
                password='123'
            )

    def test_create_superuser(self):
        """Test if a superuser can be successfully created"""
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com',
            first_name='super',
            last_name='user',
            password='123'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
