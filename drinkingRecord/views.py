from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F, Avg, Count
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from collections import Counter
from .models import AlcoholRecord, AlcoholType
from .serializers import AlcoholRecordSerializer

# 음주 기록을 생성하고 조회하는 API
class AlcoholRecordListCreateView(generics.ListCreateAPIView):
    queryset = AlcoholRecord.objects.all()
    serializer_class = AlcoholRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자에 대한 음주 기록 필터링
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 새로운 음주 기록 생성 시 사용자 정보를 포함하여 저장
        serializer.save(user=self.request.user)

# 날짜별로 음주 측정량을 계산해주는 API
class MonthlyAlcoholConsumption(APIView):
    permission_classes = [IsAuthenticated]

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

# 사용자의 음주 패턴을 분석해주는 API
class AlcoholAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        first_day_of_month = today.replace(day=1)

        # 이번 달에 대한 분석
        monthly_records = AlcoholRecord.objects.filter(
            user=user,
            date__gte=first_day_of_month,
            date__lte=today
        )

        # 음주 횟수
        monthly_drink_count = monthly_records.count()

        # 술의 종류에 따른 잔 수
        drink_type_counts = monthly_records.values('alcohol_type__name').annotate(
            total_servings=Sum('servings')
        )

        # 평균 음주 시간, 날씨, 기분
        avg_drinking_duration = monthly_records.aggregate(avg_duration=Avg('drinking_duration'))
        avg_weather = Counter(monthly_records.values_list('weather', flat=True))
        avg_mood = Counter(monthly_records.values_list('mood', flat=True))

        # 가장 많이 마신 술 종류 (이번 달)
        most_drunk_this_month = max(drink_type_counts, key=lambda x: x['total_servings'])['alcohol_type__name']

        # 최근 6개월 동안 가장 많이 마신 술 종류
        six_months_ago = today - timedelta(days=180)
        six_month_records = AlcoholRecord.objects.filter(
            user=user,
            date__gte=six_months_ago,
            date__lte=today
        ).values('alcohol_type__name').annotate(
            total_servings=Sum('servings')
        )

        most_drunk_six_months = max(six_month_records, key=lambda x: x['total_servings'])['alcohol_type__name']

        # 응답 데이터 생성
        response_data = {
            "monthly_analysis": {
                "drink_count": monthly_drink_count,
                "drink_types": list(drink_type_counts),
                "avg_drinking_duration": avg_drinking_duration['avg_duration'],
                "avg_weather": avg_weather.most_common(1)[0][0] if avg_weather else None,
                "avg_mood": avg_mood.most_common(1)[0][0] if avg_mood else None,
                "most_drunk_this_month": most_drunk_this_month,
            },
            "six_months_analysis": {
                "most_drunk_six_months": most_drunk_six_months
            }
        }

        return Response(response_data)
