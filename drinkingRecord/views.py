from rest_framework import generics
from .models import AlcoholRecord
from .serializers import AlcoholRecordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils.timezone import make_aware
from datetime import datetime

# 음주 기록하는 파트
class AlcoholRecordListCreateView(generics.ListCreateAPIView):
    queryset = AlcoholRecord.objects.all()
    serializer_class = AlcoholRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 사용자별 기록 필터링
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 사용자 정보와 함께 기록 저장
        serializer.save(user=self.request.user)

# 날짜별로 음주 측정량을 계산해주는 파트
class MonthlyAlcoholConsumption(APIView):
    def get(self, request, user_id, year, month):
        start_date = make_aware(datetime(year, month, 1))
        end_date = make_aware(datetime(year, month + 1, 1)) if month < 12 else make_aware(datetime(year + 1, 1, 1))

        records = AlcoholRecord.objects.filter(
            user_id=user_id,
            date__range=[start_date, end_date]
        ).annotate(
            total_alcohol_intake=F('servings') * F('alcohol_type__alcohol_content_per_serving')
        ).values('date').annotate(
            total_consumption=Sum('total_alcohol_intake')
        )

        response_data = {
            "year": year,
            "month": month,
            "data": list(records)
        }
        return Response(response_data)
