from django.db import models
from django.conf import settings

class SobrietyRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    savings = models.FloatField(default=0.0)
    calories_saved = models.FloatField(default=0.0)
    sobriety_goal = models.CharField(max_length=255)
    daily_memo = models.TextField(blank=True)
    average_consumption = models.FloatField(default=0.0)

    def calculate_savings_and_calories(self):
        # 평균 음주량을 기반으로 계산
        days = (self.end_date - self.start_date).days + 1
        calculated_savings = days * self.average_consumption * 1000  # 예: 1잔당 1000원의 비용으로 계산
        calculated_calories_saved = days * self.average_consumption * 70  # 예: 1잔당 70칼로리로 계산
        return calculated_savings, calculated_calories_saved

    def save(self, *args, **kwargs):
        # 계산을 호출하고 결과를 저장하기 전에 모델 필드를 업데이트
        self.savings, self.calories_saved = self.calculate_savings_and_calories()
        super().save(*args, **kwargs)  # 부모 클래스의 save 메소드 호출

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date}"
