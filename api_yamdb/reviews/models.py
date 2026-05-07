from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .constants import COMMENT_PREVIEW_LENGTH, REVIEW_PREVIEW_LENGTH


User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        Title, 
        on_delete=models.CASCADE, 
        verbose_name='Произведение')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата и время публикации отзыва', 
                                    auto_now_add=True)
    
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_per_user_title'
            )
        ]

    def __str__(self):
        return f'{self.author} - {self.text[:REVIEW_PREVIEW_LENGTH]}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField('Дата и время публикации комментария', 
                                    auto_now_add=True)
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author} - {self.text[:COMMENT_PREVIEW_LENGTH]}'