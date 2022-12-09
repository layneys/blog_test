from django.contrib.auth import get_user_model
from django.test import TestCase
from users.models import UserProfile


class DetailLoginTest(TestCase):
    def setUp(self):
        self.super_user_data = {
            'username': 'user_test',
            'email': 'test@mail.test',
            'password': 'TestPassword',
        }
        self.super_user = get_user_model().objects.create_superuser(
            **self.super_user_data
        )
        self.user_profile_data = {
            'first_name': 'Vsel',
            'last_name': 'Drog'
        }

        UserProfile.objects.create(user=self.super_user, **self.user_profile_data)

    def test_not_logged(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertContains(response, 'Login')

    def test_succ_login(self):
        response = self.client.post(
            '/login/',
            data={'username': self.super_user_data['username'],
                  'password': self.super_user_data['password'], }
        )
        self.assertEqual(302, response.status_code)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(self.user_profile_data['first_name'],
                         response.context['first_name'])
        self.assertEqual(self.user_profile_data['last_name'],
                         response.context['last_name'])
        self.assertContains(response, 'Logout')
        self.assertIn(self.user_profile_data['first_name'],
                       response.content.decode())
        self.assertIn(self.user_profile_data['last_name'],
                       response.content.decode())

    def test_fail_login(self):
        response = self.client.post(
            '/login/',
            data={'username': 'user',
                  'password': 'pass', }
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_force_login(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.super_user_data['username'],
                          password=self.super_user_data['password'])

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)

# class RealLoginTest(TestCase):
#     fixtures = ['zauth.json']
#
#     def test_users(self):
#         users = get_user_model().objects.all()
#         print(users)
