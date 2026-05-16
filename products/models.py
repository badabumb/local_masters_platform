from django.conf import settings
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ceramics', 'Керамика'),
        ('candles', 'Свечи'),
        ('textile', 'Текстиль'),
        ('jewelry', 'Украшения'),
        ('wood', 'Дерево'),
        ('cosmetics', 'Косметика'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    image = models.FileField(upload_to='products/', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
