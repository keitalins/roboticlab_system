from django.urls import path
from . import views

app_name = 'lab_reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('new/', views.report_create, name='report_create'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('<int:pk>/submit/', views.report_submit, name='report_submit'),
    path('<int:pk>/review/', views.report_review, name='report_review'),
]
