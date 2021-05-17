from django.http import response
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Notice

from .constants import *

# Create your tests here.

class MatchingAlgorithmTests(TestCase):
    """ Test modules for matching algorithm """

    client = APIClient()

    def setUp(self):
        data = {
            "first_name": "A",
            "last_name": "B",
            "alt_first_name": "a",
            "alt_last_name": "b",
            "province": "ON",
            "date_of_birth": "1992-03-12",
        }
        # create notice
        response = self.client.post('/api/notices/', data, format='json')
        self.notice_id = response.data['notice_id']

    def test_strong_match(self):
        """
        Test for strong match cases
        """
        data = {
            "first_name": "A",
            "last_name": "B",
            "province": "ON",
            "date_of_birth": "1992-03-12",
        }
        # create record
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check matching cases
        response = self.client.get('/api/matches/', format='json')
        self.assertEqual(response.data[0]['notice_id'], self.notice_id)
        self.assertEqual(response.data[0]['match_type'], STRONG_MATCH)

    def test_possible_match(self):
        """
        Test for possible match cases
        """
        data = {
            "first_name": "A",
            "last_name": "B",
            "province": "ON",
            "date_of_birth": "1987-11-02",
        }
        # create record
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check matching cases
        response = self.client.get('/api/matches/', format='json')
        self.assertEqual(response.data[0]['notice_id'], self.notice_id)
        self.assertEqual(response.data[0]['match_type'], POSSIBLE_MATCH)

    def test_weak_match(self):
        """
        Test for weak match cases
        """
        data = {
            "first_name": "A",
            "last_name": "B",
            "province": "BC",
            "date_of_birth": "1987-11-02",
        }
        # create record
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check matching cases
        response = self.client.get('/api/matches/', format='json')
        self.assertEqual(response.data[0]['notice_id'], self.notice_id)
        self.assertEqual(response.data[0]['match_type'], WEAK_MATCH)

    def test_no_match(self):
        """
        Test for no match cases
        """
        data = {
            "first_name": "X",
            "last_name": "Y",
            "province": "BC",
            "date_of_birth": "1987-11-02",
        }
        # create record
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check matching cases
        response = self.client.get('/api/matches/', format='json')
        self.assertEqual(len(response.data), 0)

    def test_for_alt_name_match(self):
        """
        Test for alternate name match cases
        """
        data = {
            "first_name": "a",
            "last_name": "b",
            "province": "ON",
            "date_of_birth": "1992-03-12",
        }
        # create record
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check matching cases
        response = self.client.get('/api/matches/', data, format='json')
        self.assertEqual(response.data[0]['notice_id'], self.notice_id)
        self.assertEqual(response.data[0]['match_type'], STRONG_MATCH)