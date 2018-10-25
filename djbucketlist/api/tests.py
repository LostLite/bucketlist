from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Bucketlist

# Create your tests here for the bucketlist model

class ModelTestCase(TestCase):

    def setUp(self):
        """Initialize variables that will be used during the tests"""
        user = User.objects.create_user(username="nerd")
        self.bucketlist_name = "My Bucket List"
        self.bucketlist = Bucketlist(name = self.bucketlist_name, owner=user)
        

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist"""
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_creates_unique_objects(self):
        """test for unique names"""
        self.bucketlist.save()
        secondBucketList = Bucketlist(name="My Bucket List")
        with self.assertRaises(IntegrityError):
            secondBucketList.save()


class ViewTestCase(TestCase):

    """Test suite for the api views"""
    def setUp(self):
        user = User.objects.create_user(username="nerd")

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        
        self.bucketlist_data = {'name':'Go to Ibiza', 'owner':user.id}
        self.response = self.client.post(reverse('create'), self.bucketlist_data, format="json")

    def test_api_can_create_bucket_list_item(self):
        """API Has create capabilities"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_bucketlist(self):
        """Test that api can get bucket list"""
        bucketlist = Bucketlist.objects.get()

        self.response = self.client.get(reverse('details', kwargs={'pk':bucketlist.id}), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertContains(self.response, bucketlist)

    def test_api_can_update_bucketlist(self):
        """Test that api can update a bucket list"""
        bucketlist = Bucketlist.objects.get()

        changedBucketlist = {'name':'This has changed'}
        self.response = self.client.put(
            reverse('details', kwargs={'pk':bucketlist.id}), 
            changedBucketlist, 
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test that api can delete a bucketlist"""
        bucketlist = Bucketlist.objects.get()
        self.response = self.client.delete(
            reverse('details', 
            kwargs={'pk':bucketlist.id}), 
            format="json", 
            follow=True)
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)