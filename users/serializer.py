from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'u_nickname',
            'u_role',
            'u_image_0',
            'u_image_1',
            'u_image_2'
        )