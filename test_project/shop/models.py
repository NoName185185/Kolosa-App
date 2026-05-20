from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    password = models.CharField(max_length=128, db_column='password_hash')
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar_path = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Автар', db_column='avatar_path')
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    def __str__(self):
        return self.username
    
class Ad(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold')
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ads',verbose_name='Продавец' )
    brand = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.CharField(max_length=200, verbose_name='Описание')
    image_path = models.ImageField(upload_to='images/cars/', null=True, blank=True, verbose_name='Изображение')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    class Meta:
        db_table = 'ads'
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'