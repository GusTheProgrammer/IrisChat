from http import client
from urllib import response
from django.http import HttpResponse
from requests import request
from rest_framework import status
from account.forms import RegistrationForm
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from account.models import Account

class BaseTest(APITestCase):

    def test_can_view_register_page_correctly(self):
        self.register_url = reverse('register')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
    
    # def test_anonymous_cannot_see_page(self):
    #     response = self.client.get(reverse("login"))
    #     self.assertEqual(response.status_code, 302)
        

    def test_authenticated_user_can_see_page(self):
        user = Account.objects.create(
            email = "test@test.com", 
            username = "John",
        )
        self.client.force_login(user=user)
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
    
    # def test_Register_View(self):
    #     user = Account.objects.create(
    #         email = "test@test.com", 
    #         username = "John",
    #     )
    #     response = HttpResponse
    #     if user.is_authenticated:
    #         response = "You are already authenticated as " + str(user.email)
    #         return response
        

