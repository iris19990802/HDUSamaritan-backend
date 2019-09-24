from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route
from django.views.decorators.csrf import csrf_exempt


from .serializer import UserSerializer
from course.serializer import CourseSerializer
from .service import UserService
from users.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @list_route(methods=['POST'])
    def login(self,request):
        
        #从前端获取数据
        req_username = request.data['req_username']
        req_password = request.data['req_password']
        print("req_username:")
        print(req_username)
        print("req_password:")
        print(req_password)
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

        #return Response(UserSerializer(request.user).data)
        return Response(UserSerializer(request.user).data)


    @list_route(methods=['GET'])
    def find_course_by_user(self,request):

        this_user = User.objects.get(username=request.user.username)
        print()
        print(this_user)
        print()

        #result_set = this_user.stu_course_st.all()
        result_set = this_user.registration_set.all() # 记得要小写Orz
        print(result_set)
        print()

        for e in result_set:
            print(e.course.c_id)

        return Response(CourseSerializer(result_set,many=True).data)
        #从前端获取数据(cookie里拿来)
        

    