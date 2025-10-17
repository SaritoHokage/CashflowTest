from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class TxType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120)
    type = models.ForeignKey('TxType', on_delete=models.PROTECT, related_name='categories')

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self) -> str:
        return f'{self.name} ({self.type.name})'


class SubCategory(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self) -> str:
        return f'{self.name} ({self.category.name})'
