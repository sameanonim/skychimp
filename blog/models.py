from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from mailing_app.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    body = models.TextField(verbose_name='Содержимое статьи')
    picture = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(verbose_name='Количество просмотров', default=0, **NULLABLE)
    published_on = models.BooleanField(default=False, verbose_name='дата публикации')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        permissions = [
            (
                'set_published_blog',
                'Can publish blog'
            )
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(transliterated_title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:record_detail', kwargs={'slug': self.slug})

    def toggle_published(self):
        self.published_on = not self.published_on
        self.save()
