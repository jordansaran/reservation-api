from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ad.models import Ads


class AdsTest(APITestCase):
    basename = 'ad'
    fixtures = ['property.json', 'ad.json']

    def test_get_ad(self):
        ads: Ads = Ads.objects.get(pk='0c7383d8-4cfe-427c-83f0-55b0df641993')
        self.assertEqual(ads.platform_rate, 250.0)
        self.assertEqual(ads.platform, 'AirBnb')

    def test_list_ads(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ad(self):
        url = reverse(f'{self.basename}-detail', args=['1f2ba0fd-688d-4e09-8735-cd2e22a704fd'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ad(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "property": "c2f099e6-bb5d-4ef2-9e99-650a6c1a45e2",
            "platform": "Vrbo",
            "platform_rate": 200.0
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ad: Ads = Ads.objects.filter(**payload).first()
        if ad:
            self.assertEqual(ad.property.uuid, "c2f099e6-bb5d-4ef2-9e99-650a6c1a45e2")
            self.assertEqual(ad.platform, "Vrbo")
            self.assertEqual(ad.platform_rate, 200.0)

