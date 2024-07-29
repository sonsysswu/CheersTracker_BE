from rest_framework import generics
from .models import AlcoholRecord
from .serializers import AlcoholRecordSerializer
from rest_framework.permissions import IsAuthenticated

class AlcoholRecordListCreateView(generics.ListCreateAPIView):
    queryset = AlcoholRecord.objects.all()
    serializer_class = AlcoholRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
