from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route
from django.views.decorators.csrf import csrf_exempt
import os

from .serializer import UserSerializer
from course.serializer import CourseSerializer,RegistrationSerializerByUser,RegistrationSerializer1,RegistrationSerializer
from .service import UserService
from users.models import User
from course.models import Course,Registration

from users.utils import load_image_file,exif_transpose

import requests

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
    def logout(self,request):
        django_logout(request)
        return Response(status=status.HTTP_200_OK)
    

    @list_route(methods=['POST'])
    def add_user(self,request):
        req_username = request.data['username']
        req_nickname = request.data['nickname']
        req_role = request.data['role']
        req_password = request.data['password']

        # 创建用户
        user = User.objects.create_user(username=req_username,password=req_password,u_role=req_role,u_nickname=req_nickname)

        # 顺便帮用户登陆
        django_login(request,user)  # 后台登陆

        return Response(UserSerializer(user).data)

    @list_route(methods=['GET'])
    def user_info(self,request):
        this_user = request.user
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)

       
        if request.user.u_role == 2: # 如果当前用户是学生
            #result_set = request.user.registration_set.all()  # registration_set 记得要小写Orz
            result_set = request.user.registration_set.filter(user=this_user,is_quit=False)
            for e in result_set:
                print(e.course)
            return Response({
                'user_info':UserSerializer(request.user).data,
                'course_info':RegistrationSerializerByUser(result_set,many=True).data
                })

        elif request.user.u_role == 1: # 如果当前用户是老师
            result_set = request.user.tea_course_st.all()
            #result_set = request.user.tea_course_st.filter(c_teacher=this_user,is_deleted=False)
            return Response({
                'user_info':UserSerializer(request.user).data,
                'course_info':CourseSerializer(result_set,many=True).data
            })
            


    @list_route(methods=['GET'])
    def course_info_student(self,request):

        this_user = request.user  # 从前端获取数据(cookie里拿来)
        print(this_user.username)
        req_course_id = request.GET['course_id']

        this_course = Course.objects.get(c_id=req_course_id)

        result = this_user.registration_set.get(user=this_user,course=this_course,is_quit=False)

        return Response(RegistrationSerializer(result).data)
    

    @list_route(methods=['GET'])
    def course_info_teacher(self,request):

        this_user = request.user
        
        if this_user.u_role == 1: # 如果当前用户是老师
            req_course_id = request.GET['course_id']
            this_course = Course.objects.get(c_id=req_course_id)
            print(this_course)
            # 查找属于当前课程的所有学生，在这门课的信息

            return Response(RegistrationSerializer1(this_course).data)

    @list_route(methods=['GET'])
    def quit_course_student(self,request):
        course_id = request.GET['course_id']
        this_course = Course.objects.get(c_id=course_id)
        this_user = request.user

        # 逻辑删除
        this_regis = Registration.objects.get(user=this_user,course=this_course)
        this_regis.is_quit = True
        this_regis.save()

        return Response("Success")

    # 学生上传图片 （一次上传一张）
    @list_route(methods=['POST'])
    def upload_user_photo(self,request):

        # 获取请求的用户
        this_user = request.user
        
        # 获取此次更新照片的方向（0/1/2:正面/左侧面/右侧面）
        this_pos = request.data['pos']

        # 获取并存储图片
        this_image = request.FILES['file'] # 获取UploadedFile 对象

        # 转换图片方向
        converted_image = load_image_file(request.FILES['file'].file)

        this_image.file = converted_image

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

        # 只有此学生三张照片已齐，才通知算法端处理三张照片
        params = {}
        params['sid'] = this_user.username

        # 初始化
        status = 0
        requested = 0
        if(user_object.u_image_0 != None and user_object.u_image_1 != None and user_object.u_image_2 != None):
            
            requested = 1

            response = requests.get('http://0.0.0.0:5002/key/',json=params,timeout=60)  # 设置超时时间：永远等待（不要反复请求）
            
            status = json.loads(response.text.strip('\0'))['result'] # 0 成功 ； 1 照片文件不存在 ； 2 照片质量太差

            # 打出调试信息
            status_code = response.status_code
            json_content = response.text

            print("-------------- 请求算法端处理图片 --------------")
            print("status_code: ")
            print(status_code)
            print("json_content: ")
            print(json_content)
            
        
        return Response(
            {
                'requested': requested, #是否请求过算法端
                'status':status #算法端返回值
            })