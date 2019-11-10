from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route


from course.models import Course,Registration

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    @list_route(methods=['POST'])
    def add_course(self,request):

        # 获取请求参数：所需添加的课程数据
        this_course_code = request.data['course_code']
        this_course_name = request.data['course_name']

        # 获取请求的用户
        this_user = request.user

        if this_user.u_role != 1:   #如果用户角色不是教师，直接返回
            return Response("Error: user permission denied")

        
        # 在course表新建表项
        Course.objects.create(c_code=this_course_code,c_name=this_course_name,c_teacher=this_user)

        return Response("Success",status = status.HTTP_200_OK)
        


    @list_route(methods=['POST'])
    def register_course_student(self,request):

        # 获取请求参数：要加入的课程的course_code
        this_course_code = request.data['course_code']
        print(this_course_code)
        if(Course.objects.filter(c_code=this_course_code).exists() == True):
            this_course = Course.objects.get(c_code=this_course_code)
        else:
            return Response("Course Not Exist")
        

        # 获取请求的用户
        this_user = request.user
        
        if this_user.u_role != 2:   #如果用户角色不是学生，直接返回
            return Response("Error: user permission denied")

        # 在registration表新建表项
        # 情况一：表项已存在只是逻辑删除
        if(Registration.objects.filter(user = this_user,course = this_course).exists() == True): 
            this_regist = Registration.objects.get(user = this_user,course = this_course)
            this_regist.is_quit = False
            this_regist.save()
        # 情况二：表项不存在
        else:
            this_regist = Registration.objects.create(user=this_user,course = this_course)
            # cnt_abcense 初始为
            this_regist.cnt_abcense = this_course.cnt_sign
            print(this_course.cnt_sign)
            this_regist.save()
    
        return Response("Success",status = status.HTTP_200_OK)