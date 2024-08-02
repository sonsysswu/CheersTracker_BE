from django.db import models
from django.conf import settings

def get_default_alcohol_type():
    # 기본 AlcoholType 인스턴스를 찾거나 생성
    default_type, created = AlcoholType.objects.get_or_create(
        name='기본',  # 'Default' 대신 적절한 기본값 이름 설정
        defaults={'alcohol_content_per_serving': 0.0}  # 기본 알코올 함량 설정
    )
    return default_type.id  # 객체의 ID 반환

class AlcoholType(models.Model):
    DRINK_CHOICES = [
        ('맥주', '맥주'),
        ('소주', '소주'),
        ('과실주', '과실주'),
        ('기타주', '기타주'),
        ('증류주', '증류주'),
        ('발효주', '발효주'),
    ]
    name = models.CharField(max_length=50, choices=DRINK_CHOICES)
    alcohol_content_per_serving = models.FloatField()  # 잔 당 알코올 함량(g)

    def __str__(self):
        return f"{self.name} - {self.alcohol_content_per_serving}g per serving"

class AlcoholRecord(models.Model):
    WEATHER_CHOICES = [
        ('좋음', '좋음'),
        ('보통', '보통'),
        ('나쁨', '나쁨'),
    ]

    MOOD_CHOICES = [
        ('좋음', '좋음'),
        ('보통', '보통'),
        ('나쁨', '나쁨'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    alcohol_type = models.ForeignKey(AlcoholType, on_delete=models.CASCADE, default=get_default_alcohol_type)
    servings = models.PositiveIntegerField()  # 섭취량 (잔 수)
    drinking_duration = models.CharField(max_length=10)  # 예: "1시간"
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    memo = models.TextField(blank=True)

    def calculate_total_alcohol_intake(self):
        # 섭취한 알코올의 총 그램 수 계산
        return self.servings * self.alcohol_type.alcohol_content_per_serving

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.alcohol_type.name} - {self.calculate_total_alcohol_intake()}g"
