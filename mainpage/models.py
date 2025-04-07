from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Периоды повторения задач
PERIODS = [
    ("Y", "year"),
    ("M", "month"),
    ("d", "day"),
    ("h", "hour"),
    ("n", "never"),
]

class Geoposition(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"Lat: {self.lat}, Lon: {self.lon}"

# Модель задачи
class Task(models.Model):
    PERIODS = PERIODS
    
    owner = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.CASCADE,
        null=False
    )
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    geop = models.ForeignKey(Geoposition, on_delete=models.CASCADE, null=True, blank=True)  # Исправлено
    date_start = models.DateTimeField()
    deadline = models.DateTimeField()
    repeat_type = models.CharField(max_length=10, choices=PERIODS, default="d")
    repeat_i = models.IntegerField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def is_overdue(self):
        return self.deadline < timezone.now() and not self.done

    def is_repeat_due(self):
        """Проверяет, нужно ли повторить задачу в зависимости от типа повторения"""
        if self.repeat_type == 'Y':
            return self.deadline <= timezone.now() - timedelta(days=365 * self.repeat_i)
        elif self.repeat_type == 'M':
            return self.deadline <= timezone.now() - timedelta(days=30 * self.repeat_i)
        elif self.repeat_type == 'd':
            return self.deadline <= timezone.now() - timedelta(days=self.repeat_i)
        elif self.repeat_type == 'h':
            return self.deadline <= timezone.now() - timedelta(hours=self.repeat_i)
        return False

    def next_repeat(self):
        """Возвращает следующую дату повторяющейся задачи"""
        if self.repeat_type == 'Y':
            return self.deadline + timedelta(days=365 * self.repeat_i)
        elif self.repeat_type == 'M':
            return self.deadline + timedelta(days=30 * self.repeat_i)
        elif self.repeat_type == 'd':
            return self.deadline + timedelta(days=self.repeat_i)
        elif self.repeat_type == 'h':
            return self.deadline + timedelta(hours=self.repeat_i)
        return None

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username