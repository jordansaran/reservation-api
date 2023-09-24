from rest_framework.serializers import ModelSerializer

from booking.models import Booking


class BookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        fields = ['code', 'ad', 'check_in', 'check_out', 'comment', 'number_guests',
                  'total_price', 'created_at', 'updated_at']
