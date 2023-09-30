from rest_framework import serializers
from .models import UserPoints

class UserPointsSerilizers(serializers.ModelSerializer):
    class Meta:
        model = UserPoints
        fields = ['username', 'points', 'steps'] 