from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route


from course.models import Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    