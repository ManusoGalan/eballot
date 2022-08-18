from datetime import datetime, timedelta
from unicodedata import name
from unittest.mock import patch
from urllib import response

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from rest_framework import status

from .serializers import BallotBoxSerializer, CandidateSerializer

from .models import BallotBox, Candidate

# Create your tests here.

class BallotListTest(APITestCase):
    def test_get_ballot_list(self):
        response = self.client.get('/api/ballot')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class BallotViewTest(APITestCase):
    def test_get_inexistent_ballot(self):
        response = self.client.get('/api/ballot/1')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_ballot(self):
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/ballot/1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class BallotCreateTest(APITestCase):
    def test_create_ballot_with_early_initTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() - timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'initTimestamp': initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'endTimestamp': endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot_with_early_endTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=11)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'initTimestamp': initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'endTimestamp': endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'initTimestamp': initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'endTimestamp': endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot_with_ok_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'initTimestamp': initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'endTimestamp': endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class BallotUpdateTest(APITestCase):
    def test_update_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id + 1), {
            'name': 'Test 2'
        })
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_started_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() - timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'name': 'Test 2'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_early_initTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        newInitTimestamp = datetime.now() - timedelta(hours=1)
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'initTimestamp': newInitTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_early_endTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        newEndTimestamp = initTimestamp - timedelta(hours=1)
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'initTimestamp': newEndTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'name': ''
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_ok_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'name': 'Test 2'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BallotDeleteTest(APITestCase):
    def test_delete_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.delete('/api/ballot/' + str(ballot.id + 1))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()
        
        response = self.client.delete('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
class CandidateListTest(APITestCase):
    def test_get_candidate_inexistent_ballot(self):
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/candidate/' + str(ballot.id + 1))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_candidate_ballot(self):
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/candidate/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class CandidateCreateTest(APITestCase):
    def test_create_candidate_for_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()

        response = self.client.post('/api/candidate/' + str(ballot.id), {
            'name': 'Test Candidate',
            'imgPath' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_candidate_for_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()

        response = self.client.post('/api/candidate/' + str(ballot.id), {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        ballot.save()

        response = self.client.post('/api/candidate/' + str(ballot.id), {
            'name': 'Test Candidate',
            'imgPath' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class CandidateDeleteTest(APITestCase):
    def test_delete_inexistent_or_existent_candidate_for_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidate/' + str(ballot.id + 1) + str(candidate.id))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_inexistent_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidate/' + str(ballot.id) + str(candidate.id + 1))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        initTimestamp = datetime.now() + timedelta(hours=1)
        endTimestamp = datetime.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            initTimestamp = initTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            endTimestamp = endTimestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            imgPath = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballotParent = ballot
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidate/' + str(ballot.id) + str(candidate.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    