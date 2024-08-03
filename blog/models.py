from django.conf import settings
from django.db import models
from utils.const import NULLABLE


class BlogMod(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Заголовок поста")
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name="Ссылка для поста")
    content = models.TextField(verbose_name="Содержимое поста")
    preview_image = models.ImageField(upload_to="blog/", verbose_name="Превью поста (изображение)", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']
        permissions = [
            ('can_publish_post', 'Могу опубликовать пост'),
            ('can_edit_post', 'Могу редактировать пост'),
        ]

    def __str__(self):
        return self.title
