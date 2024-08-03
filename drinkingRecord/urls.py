from django.urls import path
from .views import AlcoholRecordListCreateView, MonthlyAlcoholConsumption, AlcoholAnalysisView

urlpatterns = [
    path('records/', AlcoholRecordListCreateView.as_view(), name='record-list-create'),
    path('calendar/', MonthlyAlcoholConsumption.as_view(), name='calendar'),
    path('api/alcohol/analysis/', AlcoholAnalysisView.as_view(), name='alcohol-analysis'),
]
