from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.user_notifications, name='user-notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark-notification-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark-all-notifications-read'),
    path('notification-preferences/', views.notification_preferences, name='notification-preferences'),
]