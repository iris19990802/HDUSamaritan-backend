from django.shortcuts import render
import time
import json
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Attendance,student_attendance
from course.models import Course,Registration

import requests

class attendanceViewSet(viewsets.ModelViewSet):

    queryset = Attendance.objects.all() # 如果没有这个，会报错: “assert queryset is not None”

    # 用户按下“发送签到照片”时，调用此API
    @list_route(methods=['POST'])
    def sign_quest(self,request): 

        # 取得“要签到的班级号”
        course_id = request.data['course_id']
        this_course = Course.objects.get(c_id = course_id)

        # 获取请求的用户
        this_user = request.user
        print(this_user)
        if(this_user.u_role != "1" and this_user.tea_course_st.filter(c_teacher=this_user).exists() == True):
            print("是教师,确实教这门课")
        else:
            return Response("Error") # 越权访问，返回error

        # 获取并存储图片
        this_image = request.FILES['file'] # UploadedFile 对象
        filename = this_image.name # 上传的照片的文件名
        enddress = filename.split('.')[-1] #文件名后缀
        file_path = 'static/input.%s'% (enddress) # 生成完整文件路径

        with open(file_path, 'wb+') as destination: # 存到/static/input.后缀 文件下
            for chunk in this_image.chunks():
                destination.write(chunk)

        # 处理算法部分所需参数：此班级内所有学生的：学号-名字  （生成字典格式）
        params = {}
        class_student_set = Registration.objects.filter(course=this_course) 
        for e in class_student_set:
            params[e.user.username] = e.user.u_nickname

        print(params)
        #post_params = json.dumps(params) # 不用转成字符串

        # 调用算法部分api  
        response = requests.post('http://192.168.249.151:6000/uploader',json=params) # 指定post请求头：application/json
        # response = requests.post('http://192.168.249.151:6000/uploader',data=post_params)
        # response = requests.post('http://192.168.249.151:6000/uploader',headers={'Content-Type': 'application/json'},data=params)
        
        # 接到返回值：“缺课学生学号”的列表
        student_abcense_lst = json.loads(response.text)

        # 处理出：全班学生的到课情况json，
        # 格式：{
        #         'username':,
        #         'nickname':,
        #         'is_abcense':0/1;
        # }
        student_sign_list = []
        for e in class_student_set:
            dirc = {}
            dirc['username'] = e.user.username
            dirc['nickname'] = e.user.u_nickname
            if e.user.username in student_abcense_lst:     # 如果列表中存在该元素
                dirc['abcense'] = 0
            else:
                dirc['abcense'] = 1
            student_sign_list.append(dirc)
         

        # 判断拍照质量：
        # 识别人数少于班级人数1/3，则建议重拍，返回json中“quantity”属性值为“low”
        if(len(student_abcense_lst) > len(params)*2/3):
            this_quantity = "low"
        else:
            this_quantity = "high"

        # 返回json格式：
        # {
        #     quantity:"low"/"high"
        #     student_sign_list:[{
        #         'username':,
        #         'nickname':,
        #         'abcense':0/1;  (1表示到了，0表示未到)
        #     }]
        # }

        return Response({
            "quantity":this_quantity,
            "student_sign_list":student_sign_list
        })


    # 用户手动修改，并“确认到课情况”后，才会真正把数据写入 abcense 数据库
    @list_route(methods=['POST'])
    def confirm_sign(self,request): 
        #Attendance.objects.create(A_course = this_course) # 为当前“签到”，在 Attendance 表里创建一个表项
        # for e in Attendance.objects.all():
        #     print(e.id)
        #     print(e.A_course)
        return Response("1")
        

