from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start_conversation/', views.start_conversation, name='start_conversation'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]
