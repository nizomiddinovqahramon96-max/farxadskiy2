from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Elon(models.Model):
    BRAND_CHOICES = (
        ('Chevrolet', 'Chevrolet'),
        ('BYD', 'BYD'),
        ('Kia', 'Kia'),
        ('Hyundai', 'Hyundai'),
        ('Chery', 'Chery'),
    )
    COLOR_CHOICES = (
        ('Black', 'Black'),
        ('White', 'White'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Silver', 'Silver'),
    )
    MOTOR_CHOICES = (
        ('Electr', 'Electr'),
        ('Benzin', 'Benzin'),
        ('Gibrid', 'Gibrid'),
        ('Metan', 'Metan'),
        ('Propan', 'Propan'),
    )
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    km = models.PositiveIntegerField()
    xolat = models.CharField(max_length=100)
    motor = models.CharField(max_length=100, choices=MOTOR_CHOICES)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='elons')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ImageElon(models.Model):
    elon = models.ForeignKey(Elon, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='elon_images/')


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    elon = models.ForeignKey(Elon, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'elon')

    def __str__(self):
        return f'{self.user} liked {self.elon}'