from django.contrib.auth import get_user_model
from django.test import TestCase

from django.utils.translation import gettext_lazy as _
from users.models import UserProfile
from posts.models import Post


class UserRegisterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_data = {
            'username': 'test_reg',
            'email': 'reg@test.test',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Roflan',
            'last_name':'Test',
        }
        cls.post_creation_data = {
            'title':'A very interesting title',
            'body': 'Yup, a more interesting body'
        }
        cls.post_upd_data = {
            'title':'Lorem Ipsum123',
            'body': 'Dunno what'
        }
        cls.post_err_upd_ntitle_data = {
            'title':'',
            'body': 'Dunno what'
        }
        cls.post_err_upd_nbody_data = {
            'title':'Lorem Ipsum123',
            'body': ''
        }

    def test_succ_update(self):
        response = self.client.post(
            '/user/create/',
            data=self.author_data
        )
        self.assertEqual(302, response.status_code)

        self.client.login(username=self.author_data['username'],
                          password=self.author_data['password1'])

        new_user = get_user_model().objects.get(
            username=self.author_data['username']
        )

        author = UserProfile.objects.get(user=new_user)

        self.post_creation_data['author'] = UserProfile.objects.get(user=new_user)

        response = self.client.post(
            '/posts/create/',
            data=self.post_creation_data
        )

        response = self.client.get('/')


        post = Post.objects.filter(author=author).first()

        self.assertContains(response, self.post_creation_data['title'])
        self.assertContains(response, self.post_creation_data['body'])

        response = self.client.post(
            f'/posts/update/{post.id}/',
            data=self.post_upd_data
        )

        self.assertEqual(302, response.status_code)

        response = self.client.get('/')

        self.assertContains(response, self.post_upd_data['title'])
        self.assertContains(response, self.post_upd_data['body'])

        self.assertEqual(author.user, post.author.user)
        self.assertEqual(author, post.author)


    def test_fail_create_ntitle(self):
        response = self.client.post(
            '/user/create/',
            data=self.author_data
        )
        self.assertEqual(302, response.status_code)

        self.client.login(username=self.author_data['username'],
                          password=self.author_data['password1'])

        new_user = get_user_model().objects.get(
            username=self.author_data['username']
        )

        author = UserProfile.objects.get(user=new_user)

        self.post_creation_data['author'] = UserProfile.objects.get(user=new_user)

        response = self.client.post(
            '/posts/create/',
            data=self.post_creation_data,
        )

        response = self.client.get('/')

        post = Post.objects.filter(author=author).first()

        response = self.client.post(
            f'/posts/update/{post.id}/',
            data=self.post_err_upd_ntitle_data
        )

        self.assertEqual(200, response.status_code)

        response = self.client.get('/')

        self.assertNotContains(response, self.post_err_upd_ntitle_data['body'])

    def test_fail_create_nbody(self):
        response = self.client.post(
            '/user/create/',
            data=self.author_data
        )
        self.assertEqual(302, response.status_code)

        self.client.login(username=self.author_data['username'],
                          password=self.author_data['password1'])

        new_user = get_user_model().objects.get(
            username=self.author_data['username']
        )

        author = UserProfile.objects.get(user=new_user)

        self.post_creation_data['author'] = UserProfile.objects.get(user=new_user)

        response = self.client.post(
            '/posts/create/',
            data=self.post_creation_data,
        )

        response = self.client.get('/')

        post = Post.objects.filter(author=author).first()

        response = self.client.post(
            f'/posts/update/{post.id}/',
            data=self.post_err_upd_nbody_data
        )

        self.assertEqual(200, response.status_code)

        response = self.client.get('/')

        self.assertNotContains(response, self.post_err_upd_nbody_data['title'])



