from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from property.models import Property


class PropertyTest(APITestCase):
    basename = 'property'
    fixtures = ["property.json"]

    def test_get_property(self):
        property: Property = Property.objects.get(pk='52d3ca4c-141f-4d15-9908-c99459071ff3')
        self.assertEqual(property.pets_allowed, True)

    def test_list_properties(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_properties(self):
        url = reverse(f'{self.basename}-detail', args=['52d3ca4c-141f-4d15-9908-c99459071ff3'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_properties(self):
        url = reverse(f'{self.basename}-detail', args=['52d3ca4c-141f-4d15-9908-c99459071ff3'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_properties(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "guest_limit": 3,
            "number_bathrooms": 2,
            "pets_allowed": False,
            "cleaning_cost": 120.0,
            "activation_date": date.today().isoformat()
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        property: Property = Property.objects.filter(**payload).first()
        if property:
            self.assertEqual(property.guest_limit, 3)
            self.assertEqual(property.number_bathrooms, 2)
            self.assertEqual(property.pets_allowed, False)
            self.assertEqual(property.cleaning_cost, 120.0)
            self.assertEqual(property.activation_date.isoformat(), date.today().isoformat())
