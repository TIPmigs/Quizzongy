from django.urls import path
from .views import (
    admin_quiz_create_view,
    admin_quiz_update_view,
    quiz_view,
)

urlpatterns = [
    path('create/', admin_quiz_create_view, name='create_quiz'),
    path('<int:id>/edit/', admin_quiz_update_view, name='edit_quiz'),
    path('<int:id>/', quiz_view, name="view_quiz"),
]