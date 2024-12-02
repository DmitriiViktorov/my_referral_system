from rest_framework import serializers
from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    referred_users = serializers.ListField(
        child=serializers.CharField(),
        source='get_referred_users',
        read_only=True
    )
    class Meta:
        model = MyUser
        fields = ['phone_number', 'invite_code', 'referred_by', 'referred_users']


