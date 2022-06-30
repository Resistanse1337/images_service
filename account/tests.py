from django.test import TestCase
from django.urls import reverse
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test.client import Client

from rest_framework.test import APITestCase

from .models import *
from .serializers import *


LOGIN = "Alex"
PASSWORD = "123"


def create_user():
    user = User.objects.create(username=LOGIN, email="alex@mail.ru")
    user.set_password(PASSWORD)
    user.save()

    return user


class ImagesTestCase(APITestCase):
    def test_get(self):
        user = create_user()
        image1 = Image.objects.create(user=user, image="123")

        response = self.client.get(reverse("image_with_user_id", args=(user.id, )))

        serializer = ImageSerializer([image1], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer, response.data)

    def test_post(self):
        user = create_user()

        self.client.login(username=LOGIN, password=PASSWORD)

        file = File(open(settings.TMP_IMAGE_PATH, 'rb'))
        uploaded_file = SimpleUploadedFile("tmp", file.read(),
                                               content_type='multipart/form-data')

        response = self.client.post(reverse("image_with_user_id", args=(user.id, )),
                                    {'image': uploaded_file}, format='multipart')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        user = create_user()

        image = Image.objects.create(user=user, image="123")

        login = self.client.login(username=LOGIN, password=PASSWORD)

        self.assertEqual(login, True)

    def test_delete(self):
        user = create_user()

        image = Image.objects.create(user=user, image="123")

        self.client.login(username=LOGIN, password=PASSWORD)

        response = self.client.delete(reverse("image_with_user_id", args=(user.id, )), )

        self.assertEqual(response.status_code, 200)


class UsersTestCase(APITestCase):
    def test_get(self):
        user = create_user()

        self.client.login(username=LOGIN, password=PASSWORD)

        response = self.client.get(reverse("get_user"))

        self.assertEqual({'username': 'Alex', 'email': 'alex@mail.ru', 'first_name': '', 'last_name': ''},
                         response.data)


