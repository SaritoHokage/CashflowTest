from django.contrib import admin
from django import forms
from .models import Status, TxType, Category, SubCategory

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Подписи в селекте для ForeignKey type
        self.fields['type'].label_from_instance = lambda obj: obj.name

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(TxType)
class TxTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
