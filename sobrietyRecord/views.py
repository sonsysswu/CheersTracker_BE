from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SobrietyRecord
from .serializers import SobrietyRecordSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def set_average_consumption(request):
    if request.method == 'POST':
        user = request.user
        average_consumption = request.data.get('average_consumption', 0.0)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        goal = request.data.get('sobriety_goal')

        record = SobrietyRecord.objects.create(
            user=user,
            start_date=start_date,
            end_date=end_date,
            average_consumption=average_consumption,
            sobriety_goal=goal
        )
        serializer = SobrietyRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
