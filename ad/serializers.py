from rest_framework.serializers import ModelSerializer

from ad.models import Ads


class AdsSerializer(ModelSerializer):

    class Meta:
        model = Ads
        fields = '__all__'
