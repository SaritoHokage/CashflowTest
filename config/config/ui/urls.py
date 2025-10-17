print('LOADED ui.urls')
from django.urls import path
from .views import (
    home, entries_list, entry_create, entry_edit,
    categories_options, subcategories_options,
    entry_delete, entry_duplicate, entries_export_csv
)
urlpatterns = [
    path('', home, name='home'),
    path('entries/', entries_list, name='entries_list'),
    path('entries/new/', entry_create, name='entry_create'),
    path('entries/<int:pk>/edit/', entry_edit, name='entry_edit'),
    path('entries/<int:pk>/delete/', entry_delete, name='entry_delete'),
    path('entries/<int:pk>/dup/', entry_duplicate, name='entry_duplicate'),
    path('entries/export/csv/', entries_export_csv, name='entries_export_csv'),
    path('hx/categories/', categories_options, name='hx_categories'),
    path('hx/subcategories/', subcategories_options, name='hx_subcategories'),
]
