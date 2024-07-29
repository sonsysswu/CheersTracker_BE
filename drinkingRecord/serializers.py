from rest_framework import serializers
from .models import AlcoholRecord

class AlcoholRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlcoholRecord
        fields = '__all__'
