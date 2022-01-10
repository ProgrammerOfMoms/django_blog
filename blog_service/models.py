from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """Модель поста"""
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    )
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    slug = models.SlugField(max_length=256, unique_for_date='publish', verbose_name='Слаг')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = models.TextField(verbose_name='Текст публикации')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публицации'
    
    def get_absolute_url(self):
        return reverse('blog_service:post_detail', args=[self.publish.year,
                                                         self.publish.month,
                                                         self.publish.day,
                                                         self.slug])
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Публикация')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    body = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=timezone.now, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=timezone.now, verbose_name='Обновлен')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
