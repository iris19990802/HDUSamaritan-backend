from .models import Course
from rest_framework import serializers

from users.serializer import UserSerializer
class CourseSerializer(serializers.ModelSerializer):
    c_teacher = UserSerializer()
    class Meta:
        model = Course
        fields = (
            'c_id',
            'c_name',
            'c_teacher',
        )