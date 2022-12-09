from django.contrib.auth import get_user_model
from django.test import TestCase
from users.models import UserProfile
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile


class UserRegisterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_start_data = {
            'username': 'test_reg',
            'email': 'reg@test.test',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Roflan',
            'last_name': 'Test',
            'bio': 'Заходят как-то в бар...'
        }
        cls.user_update_data = {
            'first_name': 'Ihope',
            'last_name': 'Itworks',
            'bio': 'Не заходят...'
        }
        cls.user_upd_empty_fname = {
            'first_name': '',
            'last_name': 'Itworks',
            'bio': 'Не заходят...'
        }
        cls.user_upd_empty_lname = {
            'first_name': 'Ihope',
            'last_name': '',
            'bio': 'Не заходят...'
        }



    def test_succ_update(self):
        response = self.client.post(
            '/user/create/',
            data=self.user_start_data
        )
        self.assertEqual(302, response.status_code)

        new_user = get_user_model().objects.get(
            username=self.user_start_data['username']
        )

        self.assertEqual(self.user_start_data['email'],
                         new_user.email)

        self.client.login(username=self.user_start_data['username'],
                          password=self.user_start_data['password1'])

        response = self.client.get('/')

        user_profile_id_before_upd = response.context['user_id']

        user_profile_before_upd = UserProfile.objects.get(user=new_user)

        data_before_upd = {
            'user_profile_id': response.context['user_id'],
            'first_name': user_profile_before_upd.first_name,
            'last_name': user_profile_before_upd.last_name,
            'bio': user_profile_before_upd.bio,
        }

        response = self.client.post(
            f'/user/{user_profile_id_before_upd}/update/',
            self.user_update_data,
        )

        self.assertEqual(302, response.status_code)

        response = self.client.get('/')

        user_profile_after_upd = UserProfile.objects.get(user=new_user)

        data_after_upd = {
            'user_profile_id': response.context['user_id'],
            'first_name': user_profile_after_upd.first_name,
            'last_name': user_profile_after_upd.last_name,
            'bio': user_profile_after_upd.bio,
        }

        # print(data_before_upd['bio'])
        # print(data_after_upd['bio'])

        self.assertEqual(data_before_upd['user_profile_id'], data_after_upd['user_profile_id'])
        self.assertNotEqual(data_before_upd['first_name'], data_after_upd['first_name'])
        self.assertNotEqual(data_before_upd['last_name'], data_after_upd['last_name'])
        self.assertNotEqual(data_before_upd['bio'], data_after_upd['bio'])

    def test_fail_upd_empty_fname(self):
        response = self.client.post(
            '/user/create/',
            data=self.user_start_data
        )
        self.assertEqual(302, response.status_code)

        new_user = get_user_model().objects.get(
            username=self.user_start_data['username']
        )

        self.assertEqual(self.user_start_data['email'],
                         new_user.email)

        self.client.login(username=self.user_start_data['username'],
                          password=self.user_start_data['password1'])

        response = self.client.get('/')

        user_profile_id_before_upd = response.context['user_id']

        user_profile_before_upd = UserProfile.objects.get(user=new_user)

        response = self.client.post(
            f'/user/{user_profile_id_before_upd}/update/',
            self.user_upd_empty_fname,
        )
        self.assertEqual(response.status_code, 200)


    def test_fail_upd_empty_lname(self):
        response = self.client.post(
            '/user/create/',
            data=self.user_start_data
        )
        self.assertEqual(302, response.status_code)

        new_user = get_user_model().objects.get(
            username=self.user_start_data['username']
        )

        self.assertEqual(self.user_start_data['email'],
                         new_user.email)

        self.client.login(username=self.user_start_data['username'],
                          password=self.user_start_data['password1'])

        response = self.client.get('/')

        user_profile_id_before_upd = response.context['user_id']

        user_profile_before_upd = UserProfile.objects.get(user=new_user)

        response = self.client.post(
            f'/user/{user_profile_id_before_upd}/update/',
            self.user_upd_empty_lname,
        )
        self.assertEqual(response.status_code, 200)

