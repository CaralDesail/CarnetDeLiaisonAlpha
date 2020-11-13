from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('notificationsAView/', views.NotifList.as_view(template_name='notifications/notifications_list.html'), name="notificationsAView"),
    ]