from django.urls import path
from . import views

app_name = 'messaging_app'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('<int:pk>/reply/', views.reply, name='reply'),
    path('notifications/', views.notifications, name='notifications'),
]
