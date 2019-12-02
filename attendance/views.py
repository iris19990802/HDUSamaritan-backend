from django.shortcuts import render
import time
import json
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Attendance,student_attendance
from course.models import Course,Registration
from users.models import User
import requests
import os
import re
from config.settings import BASE_DIR


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
        if(this_user.u_role != "1" and this_user.tea_course_st.filter(c_teacher=this_user).exists() == True):
            pass
            #print("是教师,确实教这门课")
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

        # 处理算法部分所需参数：此班级内所有学生的：学号 （列表）
        params = []
        class_student_set = Registration.objects.filter(course=this_course) 
        for e in class_student_set:
            params.append(e.user.username)

        print(params)
        #post_params = json.dumps(params) # 不用转成字符串

        # 调用算法部分api (sign)
        #response = requests.post('http://host.docker.internal:6000/uploader',json=params) # 指定post请求头：application/json
        #response = requests.post('http://172.17.0.1:6000/uploader',json=params)

        #response = requests.post('http://x.b1n.top:12350/query/',json=params)

        response = requests.post('http://0.0.0.0:5002/query/',json=params)

        print("-------------- 请求算法端签到（query）-----------------")
        print("status_code")
        print(response.status_code)
        print("json")
        print(response.text)

        # --------------  返回值还要调过  ---------------------

        result_type = response.text['result']
       
        # 接到返回值：“缺课学生学号”的列表
        student_abcense_lst = response.text['miss']
        #student_abcense_lst = json.loads(response.text)

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


        # 找出 output 文件的真正路径（本来后缀未知）
        output_photo_name = ""
        rootdir = os.path.join(BASE_DIR, "static")
        print(rootdir)
        list = os.listdir(rootdir)
        for i in range(0, len(list)):
            if re.match('^output*',list[i])!=None:
                output_photo_name = list[i]
                break
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
            "student_sign_list":student_sign_list,
            "output_photo_src":'static/'+output_photo_name
        })


    # 用户手动修改，并“确认到课情况”后，才会真正把数据写入 abcense 数据库
    @list_route(methods=['POST'])
    def confirm_sign(self,request):
        course_id = request.data['course_id']
        this_course = Course.objects.get(c_id = course_id)
        print(course_id)

        student_list = request.data['user_abcense']
        print(student_list)

        # 创建新的“签到”对象
        this_attendance = Attendance.objects.create(A_course = this_course) # 为当前“签到”，在 Attendance 表里创建一个表项
        print(this_attendance.id)

        # 注册进“学生-签到”多对多表
        for e in student_list:
            this_user = User.objects.get(username=e['username'])
            this_abcense = e['abcense']
            student_attendance.objects.create(user=this_user,attendance=this_attendance,abcense=this_abcense)

        # 更新“学生-班级”表（Registration）的 cnt_abcense 数据
        for e in student_list:
            if e['abcense'] == 1: # 只有“缺课”，才能继续操作
                continue
            else: # “改”操作
                this_user = User.objects.get(username=e['username'])
                this_registration = Registration.objects.get(user=this_user,course=this_course)
                this_registration.cnt_abcense = this_registration.cnt_abcense + 1
                this_registration.save()

        # 更新班级表（Course）的 cnt_sign 数据
        this_course.cnt_sign = this_course.cnt_sign + 1
        this_course.save() # “改”操作，需要save

        return Response("1")
        

