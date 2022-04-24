import email
import imp
import profile
from django.test import TestCase
from account.models import Account, MyAccountManager
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

        
class TestAccountModels(APITestCase): # use superuser to create a user?
    def setUp(self):
        self.superuser = Account.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson'}
        self.user = Account.objects.create(
            email = "test@test.com", 
            username = "John",
        )
    
    def test_str_account(self): # test string representation of account model
        expected_outcome = "John"
        self.assertEqual(expected_outcome, str(self.user))

    def test_can_create_user(self):
        response = self.client.post(reverse('homepage'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createUser_raises_valueError_noUsername(self):
        self.assertRaises(ValueError, Account.objects.create_user,username="", email="test@test.com")

    def test_createUser_raises_valueError_noEmail(self):
        self.assertRaises(ValueError, Account.objects.create_user,username="John", email="")
    
    # def test_gettingProfileImage(self):
    #     filename = self.user.get_profile_image_image_filename()
    #     expected_outcome = 'profile_images/' + str(self.user.pk) + '/profile_image.png'
    #     self.assertEqual(expected_outcome, filename)