from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route
from django.views.decorators.csrf import csrf_exempt
import os

from .serializer import UserSerializer
from course.serializer import CourseSerializer,RegistrationSerializer
from .service import UserService
from users.models import User
from course.models import Course,Registration

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @list_route(methods=['POST'])
    def login(self,request):
        
        #从前端获取数据
        req_username = request.data['req_username']
        req_password = request.data['req_password']

        #从库里查询数据并校验
        if not UserService.check_user_exists(req_username):
            return Response({'detail':'账号不存在','field':'username'},status = status.HTTP_401_UNAUTHORIZED)

        this_user = UserService.find_by_username(req_username)
        checked_user = authenticate(username=this_user.username,password=req_password)

        if checked_user is None:
            return Response({'detail':'密码错误','field':'password'},status = status.HTTP_401_UNAUTHORIZED)
        
        # 后台登陆
        django_login(request,checked_user) 

        # 设置缓存
        remember = True
        if remember:
            request.session.set_expiry(60*60*24)
        else:
            request.session.set_expiry(0)

        return Response(UserSerializer(request.user).data)


    @list_route(methods=['GET'])
    def find_course_by_user(self,request):

        this_user = User.objects.get(username=request.user.username)  #从前端获取数据(cookie里拿来)

        if this_user.u_role == 2: # 如果当前用户是学生
            result_set = this_user.registration_set.all()  # registration_set 记得要小写Orz
            return Response(RegistrationSerializer(result_set,many=True).data)

        elif this_user.u_role == 1: # 如果当前用户是老师
            result_set = this_user.tea_course_st.all()
            return Response(CourseSerializer(result_set,many=True).data)
            # print(result_set)
            # print()
            # for e in result_set:
            #     print(e.c_id)

            


    @list_route(methods=['GET'])
    def course_info_student(self,request):

        this_user = request.user  # 从前端获取数据(cookie里拿来)
        print(this_user.username)
        req_course_id = request.GET['course_id']

        this_course = Course.objects.get(c_id=req_course_id)

        result = this_user.registration_set.get(user=this_user,course=this_course)

        return Response(RegistrationSerializer(result).data)
    

    @list_route(methods=['GET'])
    def course_info_teacher(self,request):

        this_user = request.user

        if this_user.u_role == 1: # 如果当前用户是老师
            req_course_id = request.GET['course_id']
            this_course = Course.objects.get(c_id=req_course_id)
            print(this_course)
            # 查找属于当前课程的所有学生，在这门课的信息
            result_set = Registration.objects.filter(course=this_course) 

            return Response(RegistrationSerializer(result_set,many=True).data)


    # 学生上传图片
    @list_route(methods=['POST'])
    def upload_user_photo(self,request):

        # 获取请求的用户
        this_user = request.user
        
        # 获取此次更新照片的方向（0/1/2:正面/左侧面/右侧面）
        this_pos = request.data['pos']

        # 获取并存储图片
        this_image = request.FILES['file'] # 获取UploadedFile 对象


#         # 删除已存在文件
#         if(os.path.exists(dirPath+"foo.txt")):
# 　　        os.remove(dirPath+"foo.txt")

        user_object = User.objects.get(username=this_user.username) # 按指定文件名存储图片
        
        if this_pos == "0":
            old_file_path = user_object.u_image_0 # ImageFieldFile
            if old_file_path.name != "":
                if os.path.exists(old_file_path.path):
                    os.remove(old_file_path.path)
            user_object.u_image_0 = this_image

        elif this_pos == "1":
            old_file_path = user_object.u_image_1 # ImageFieldFile
            if old_file_path.name != "":
                if os.path.exists(old_file_path.path):
                    os.remove(old_file_path.path)
            user_object.u_image_1 = this_image

        elif this_pos == "2":
            old_file_path = user_object.u_image_2 # ImageFieldFile
            if old_file_path.name != "":
                if os.path.exists(old_file_path.path):
                    os.remove(old_file_path.path)
            user_object.u_image_2 = this_image

        user_object.save()



        return Response(UserSerializer(user_object).data)