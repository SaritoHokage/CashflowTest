from django.db import models
from django.utils import timezone
from core.models import Status, TxType, Category, SubCategory
from django.core.exceptions import ValidationError

class CashFlowEntry(models.Model):
    created_at = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='entries')
    type = models.ForeignKey(TxType, on_delete=models.PROTECT, related_name='entries')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='entries')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='entries')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['type']),
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
        ]

    def clean(self):
        if self.category_id and self.type_id and self.category.type_id != self.type_id:
            raise ValidationError({'category': 'Категория не относится к выбранному типу.'})
        if self.subcategory_id and self.category_id and self.subcategory.category_id != self.category_id:
            raise ValidationError({'subcategory': 'Подкатегория не относится к выбранной категории.'})

    def __str__(self) -> str:
        return f'{self.created_at} {self.amount}'
