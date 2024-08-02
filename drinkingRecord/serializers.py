from rest_framework import serializers
from .models import AlcoholRecord, AlcoholType

class AlcoholTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlcoholType
        fields = ['name', 'alcohol_content_per_serving']

class AlcoholRecordSerializer(serializers.ModelSerializer):
    alcohol_type = AlcoholTypeSerializer(read_only=True)
    total_alcohol_intake = serializers.SerializerMethodField()

    class Meta:
        model = AlcoholRecord
        fields = [field.name for field in AlcoholRecord._meta.fields] + ['total_alcohol_intake']  

    def get_total_alcohol_intake(self, obj):
        return obj.calculate_total_alcohol_intake()

