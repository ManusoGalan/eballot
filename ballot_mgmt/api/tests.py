from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from rest_framework import status

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
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.get('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_ballot_with_candidates(self):
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['candidates'][0]["result"] is None)
        
    def test_get_finished_ballot_with_candidates(self):
        start_datetime = timezone.now() - timedelta(hours=10)
        end_datetime = timezone.now() - timedelta(hours=1)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['candidates'][0]["result"] is not None)
    
class BallotCreateTest(APITestCase):
    def test_create_ballot_with_early_initTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() - timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot_with_early_endTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=20)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        response = self.client.post('/api/ballot', {
            'name': 'Test',
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class BallotUpdateTest(APITestCase):
    def test_update_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id + 1), {
            'name': 'Test 2'
        })
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_started_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() - timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'name': 'Test 2'
        })
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_update_ballot_with_early_initTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        newInitTimestamp = timezone.now() - timedelta(hours=1)
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'start_datetime': newInitTimestamp.strftime("%Y-%m-%dT%H:%M:%S")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_early_endTimestamp(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        newEndTimestamp = start_datetime - timedelta(hours=1)
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'start_datetime': newEndTimestamp.strftime("%Y-%m-%dT%H:%M:%S")
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.patch('/api/ballot/' + str(ballot.id), {
            'name': ''
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
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
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.delete('/api/ballot/' + str(ballot.id + 1))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_started_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() - timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.delete('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_delete_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.delete('/api/ballot/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
class CandidateListTest(APITestCase):
    def test_get_candidate_inexistent_ballot(self):
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/candidates/' + str(ballot.id + 1))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_candidate_empty_ballot(self):
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()
        
        response = self.client.get('/api/candidates/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_candidate_ballot(self):
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()
        
        response = self.client.get('/api/candidates/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class CandidateCreateTest(APITestCase):
    def test_create_candidate_for_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()

        response = self.client.post('/api/candidates/' + str(ballot.id + 1), {
            'name': 'Test Candidate',
            'img_path' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_candidate_for_ballot_with_faulty_data(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()

        response = self.client.post('/api/candidates/' + str(ballot.id), {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_candidate_for_started_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() - timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()

        response = self.client.post('/api/candidates/' + str(ballot.id), {
            'name': 'Test Candidate',
            'img_path' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_create_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()

        response = self.client.post('/api/candidates/' + str(ballot.id), {
            'name': 'Test Candidate',
            'img_path' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_multiple_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        ballot.save()

        response_first_candidate = self.client.post('/api/candidates/' + str(ballot.id), {
            'name': 'Test Candidate',
            'img_path' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        response_second_candidate = self.client.post('/api/candidates/' + str(ballot.id), {
            'name': 'Test Candidate',
            'img_path' : ImageFile(open('api/test/data/empty_user.png', 'rb')),
            'description' : 'Test description for Test Candidate',
        })
        
        self.assertEqual(response_first_candidate.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second_candidate.status_code, status.HTTP_201_CREATED)
    
class CandidateDeleteTest(APITestCase):
    def test_delete_inexistent_or_existent_candidate_for_inexistent_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidates/' + str(ballot.id + 1) + '/1')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_inexistent_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidates/' + str(ballot.id) + '/1')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       
    def test_delete_candidate_for_started_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() - timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidates/' + str(ballot.id) + '/0')
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_delete_candidate_for_ballot(self):
        admin_user = User.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
        )
        
        candidate = Candidate(
            name = 'Test Candidate',
            img_path = ImageFile(open('api/test/data/empty_user.png', 'rb')),
            description = 'Test description for Test Candidate',
            ballot_parent = ballot,
            pk_inside_ballot = 0
        )
        
        ballot.save()
        candidate.save()

        response = self.client.delete('/api/candidates/' + str(ballot.id) + '/0')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
class ContratctAddressViewTest(APITestCase):
    def test_get_inexistent_ballot(self):
        response = self.client.get('/api/contract/1')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_ballot(self):
        start_datetime = timezone.now() + timedelta(hours=1)
        end_datetime = timezone.now() + timedelta(hours=10)
        
        ballot = BallotBox(
            name = 'Test',
            start_datetime = start_datetime,
            end_datetime = end_datetime,
            contract_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
        )
        
        ballot.save()
        
        response = self.client.get('/api/contract/' + str(ballot.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contract_address'], "0x71C7656EC7ab88b098defB751B7401B5f6d8976F")