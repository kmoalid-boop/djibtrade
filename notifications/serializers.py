from rest_framework import serializers
from .models import Notification, NotificationPreferences

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
