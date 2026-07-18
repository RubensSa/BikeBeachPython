from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Bicicleta


class BikeAccessControlTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='Password1234')
        self.other = User.objects.create_user(username='other', password='Password1234')
        self.bike = Bicicleta.objects.create(
            nome='Bicicleta Teste',
            modelo='Modelo A',
            valor_hora=15,
            dono=self.owner,
        )

    def test_owner_can_view_own_bike_detail(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse('rentals:bike_detail', args=[self.bike.pk]))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_view_other_bike_detail(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse('rentals:bike_detail', args=[self.bike.pk]))
        self.assertEqual(response.status_code, 404)
