from .models import Course,Registration
from rest_framework import serializers

from users.serializer import UserSerializer
class CourseSerializer(serializers.ModelSerializer):
    c_teacher = UserSerializer()
    class Meta:
        model = Course
        fields = (
            'c_id',
            'c_code',
            'c_name',
            'c_teacher',
            'cnt_sign'
        )

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()
    class Meta:
        model = Registration
        fields = (
            'user',
            'course',
            'cnt_abcense',
        )