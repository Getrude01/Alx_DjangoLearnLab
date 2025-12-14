from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    # target will be rendered as its str() representation
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "recipient", "actor", "verb", "target", "unread", "timestamp"]

    def get_target(self, obj):
        return str(obj.target) if obj.target else None