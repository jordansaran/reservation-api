from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Booking


class BookingTest(APITestCase):
    basename = 'booking'
    fixtures = ['property.json', 'ad.json', 'booking.json']

    def test_get_booking(self):
        booking: Booking = Booking.objects.get(code='6WJY4LCIQMA2COQ3')
        self.assertEqual(booking.check_in.isoformat(), '2023-10-05')
        self.assertEqual(booking.check_out.isoformat(), '2023-10-08')
        self.assertEqual(booking.total_price, 470.0)
        self.assertEqual(booking.comment, "Teste 3")
        self.assertEqual(booking.number_guests, 2)

    def test_list_booking(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_booking(self):
        url = reverse(f'{self.basename}-detail', args=['6WJY4LCIQMA2COQ3'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_booking(self):
        url = reverse(f'{self.basename}-detail', args=['6WJY4LCIQMA2COQ3'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_booking(self):
        url = reverse(f'{self.basename}-list')
        payload = {
          "ad": "1f2ba0fd-688d-4e09-8735-cd2e22a704fd",
          "check_in": "2023-10-12",
          "check_out": "2023-10-22",
          "comment": "Teste 4",
          "number_guests": 2
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking: Booking = Booking.objects.filter(**payload).first()
        if booking:
            self.assertEqual(booking.check_in.isoformat(), '2023-10-12')
            self.assertEqual(booking.check_out.isoformat(), '2023-10-22')
            self.assertEqual(booking.comment, "Teste 4")
            self.assertEqual(booking.number_guests, 2)

    def test_interval_dates_equal(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "ad": "1f2ba0fd-688d-4e09-8735-cd2e22a704fd",
            "check_in": "2023-09-23",
            "check_out": "2023-09-23",
            "comment": "Teste 5",
            "number_guests": 2
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "O CheckOut não pode ser igual a data de CheckIn")

    def test_date_past(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "ad": "1f2ba0fd-688d-4e09-8735-cd2e22a704fd",
            "check_in": "2022-09-23",
            "check_out": "2023-09-23",
            "comment": "Teste 5",
            "number_guests": 2
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('check_in', [])[0], "A data não pode ser inferior a data atual")

    def test_check_in_gather_than_check_out(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "ad": "1f2ba0fd-688d-4e09-8735-cd2e22a704fd",
            "check_in": "2024-10-23",
            "check_out": "2023-09-23",
            "comment": "Teste 5",
            "number_guests": 2
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "O CheckOut não pode ser menor que a data de CheckIn")

    def test_date_unavailable(self):
        url = reverse(f'{self.basename}-list')
        payload = {
            "ad": "0c7383d8-4cfe-427c-83f0-55b0df641993",
            "check_in": "2023-10-08",
            "check_out": "2023-10-12",
            "comment": "Teste 5",
            "number_guests": 2
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "Data indisponível para reservar, tente outro intervalo de datas")
