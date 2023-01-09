from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Напишите что-то, за что не будет стыдно'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        'Group',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='post',
        verbose_name='Группа'
    )

    class Meta:
        ordering = ('-pub_date', 'id')

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField('Имя группы', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title
