from django.urls import path

from .views import (
    add_page_info, get_page_info
)

urlpatterns = [
    path('', add_page_info),
    path('<int:object_id>', get_page_info),
]