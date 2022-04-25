import email
from django import forms
from account.forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from account.models import Account
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError


class TestAccountForms(APITestCase):
    # def setUp(self):
    #     self.user2 = Account.objects.create(
    #         email = "test1@test.com", 
    #         username = "Johnny",
    #     )

    # def test_email_is_valid(self): 
    #     with self.assertRaises(ValidationError):
    #         # not sure what these do below
    #         enquiry = Account(email="testtest.com")
    #         enquiry.full_clean()

    # def test_username_is_valid(self):
    #     with self.assertRaises(ValidationError):
    #         # not sure what these do below
    #         enquiry = Account(username="")
    #         enquiry.full_clean()

    # ^^ work but maybe pointless, and dont really improve coverage
        
    def test_RegistrationForm(self):
        form = RegistrationForm(data={
            'email': 'test@test.com',
            'username': 'John',
            'password1': 'johhny2022',
            'password2': 'johhny2022'
        })

        self.assertTrue(form.is_valid())

    def test_RegistrationForm_noDATA(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_AccountAuthenticationForm(self):
        form2 = AccountAuthenticationForm(data={
            'email': 'test@test.com',
            'password': 'johhny2022'
        })

        self.assertFalse(form2.is_valid())

    def test_AccountAuthenticationForm_noDATA(self):
        form2 = AccountAuthenticationForm(data={})

        self.assertFalse(form2.is_valid())
        self.assertEquals(len(form2.errors), 2)

    def test_AccountUpdateForm(self):
        form3 = AccountUpdateForm(data={
            'username': 'Lola',
            'email': 'test@test.com',
            'profile_image': '',
            'hide_email': 'false'
        })

        self.assertTrue(form3.is_valid())

    def test_AccountUpdateForm_noDATA(self):
        form3 = AccountUpdateForm(data={})

        self.assertFalse(form3.is_valid())
        self.assertEquals(len(form3.errors), 2)

    def test_AccountUpdateForm_save(self):
        form4 = AccountUpdateForm(data={
            'username': 'Lola',
            'email': 'test@test.com',
            'profile_image': '',
            'hide_email': 'false'
        })

        if form4.is_valid():
            form4.save()