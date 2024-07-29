from django.urls import path
from .views import SobrietyRecordListCreateView, set_average_consumption

urlpatterns = [
    path('records/', SobrietyRecordListCreateView.as_view(), name='record-list-create'),
    path('set_average_consumption/', set_average_consumption, name='set-average-consumption'),
]
