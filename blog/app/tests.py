from email.policy import HTTP
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Post, Subscribe


class PostTests(APITestCase):
    def setUp(self):

        self.user_test1 = User.objects.create_user(username="user1", password = "pas123pas")
        self.user_test2 = User.objects.create_user(username="user2", password = "qwert1234")
       
        self.user_test1_token = Token.objects.create(user = self.user_test1)
        self.user_test2_token = Token.objects.create(user = self.user_test2)
        
        self.one_post = Post.objects.create(
            title="Post1",
            content = "Post1Post1Post1Post1Post1",
            author = self.user_test1,
            time_create = "14.06.2022 06:10:32",
            time_update = "14.06.2022 06:10:32",
        )
    
        self.data_post = {
            "title":"Pos2",
            "author":"user1",
            "content":"Post2Post2",
            "time_create" : "14.06.2022 06:10:32",
            "time_update" : "14.06.2022 06:10:32",   
        }

        self.data_author = {
            "username":"user1",
            "subscriber":"user2"
        }

        self.one_subscribe =Subscribe.objects.create(
            author = self.user_test1,
            subscriber = self.user_test2
        ) 
        
    def test_create_invalid_post(self):
        response = self.client.post(reverse("post"), self.data_post, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_valid_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.post(reverse("post"), self.data_post, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_list(self):
        response = self.client.get(reverse("post"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_authors_list(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_subscribe_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test2_token.key)
        response = self.client.get(reverse("subscribe"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_post_subscribe_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test2_token.key)
        response = self.client.get(reverse("post_subscribe"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1) 


