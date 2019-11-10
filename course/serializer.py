from .models import Course,Registration
from rest_framework import serializers

from course.models import Course
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


class RegistrationSerializerByCourse(serializers.ModelSerializer):
    user = UserSerializer()
    # course = CourseSerializer()
    class Meta:
        model = Registration
        fields = (
            'user',
            # 'course',
            'cnt_abcense',
        )

class RegistrationSerializerByUser(serializers.ModelSerializer):
    #user = UserSerializer()
    course = CourseSerializer()
    class Meta:
        model = Registration
        fields = (
            #'user',
            'course',
            'cnt_abcense',
        )

class RegistrationSerializer1(serializers.ModelSerializer):
    c_teacher = UserSerializer()
    student= serializers.SerializerMethodField()

    def get_student(self, obj):
        result_set = Registration.objects.filter(course=obj) 
        return RegistrationSerializer(result_set, many=True).data

    class Meta:
        model = Course
        fields = (
            'c_id',
            'c_name',
            'c_code',
            'c_teacher',
            'cnt_sign',
            'student',
        )
    