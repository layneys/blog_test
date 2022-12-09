from django.contrib.auth import get_user_model
from django.test import TestCase

from django.utils.translation import gettext_lazy as _


class UserRegisterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {
            'username': 'test_reg',
            'email': 'reg@test.test',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Roflan',
            'last_name':'Test',
        }
        cls.user_broken_data = {
            'username': 'test_reg',
            'email': 'reg@test.test',
            'password1': 'TestPass3332',
            'password2': 'TestPass',
        }
        cls.user_simple_pass = {
            'username': 'test_reg',
            'email': 'reg@test.test',
            'password1': 'qwerty',
            'password2': 'qwerty',
        }

    def test_succ_register(self):
        response = self.client.post(
            '/user/create/',
            data=self.user_data
        )
        self.assertEqual(302, response.status_code)

        new_user = get_user_model().objects.get(
            username=self.user_data['username']
        )

        self.assertEqual(self.user_data['email'],
                         new_user.email)

    def test_fail_register(self):
        response = self.client.post(
            '/user/create/',
            data=self.user_broken_data
        )
        self.assertEqual(200, response.status_code)
        self.assertFormError(
            response,
            'form',
            'password2',
            _('The two password fields didn’t match.')
        )

        def test_fail_register_simple_pass(self):
            response = self.client.post(
                '/user/create/',
                data=self.user_simple_pass,
            )
            self.assertEqual(200, response.status_code)

            self.assertFormError(
                response,
                'form',
                'password1',
                'password2',
                errors=_("This password is too common.")
            )