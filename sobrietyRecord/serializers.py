from rest_framework import serializers
from .models import SobrietyRecord

class SobrietyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SobrietyRecord
        fields = '__all__'
