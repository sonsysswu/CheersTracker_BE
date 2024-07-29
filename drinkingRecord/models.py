from django.db import models
from django.contrib.auth.models import User

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

    DRINK_CHOICES = [
        ('맥주', '맥주'),
        ('소주', '소주'),
        ('과실주', '과실주'),
        ('기타주', '기타주'),
        ('증류주', '증류주'),
        ('발효주', '발효주'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    drink_type = models.CharField(max_length=10, choices=DRINK_CHOICES)
    quantity = models.PositiveIntegerField()
    drinking_duration = models.CharField(max_length=10)  # 예: "1시간"
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    memo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.drink_type}"
