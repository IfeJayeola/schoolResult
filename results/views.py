from django.shortcuts import render
from .models import Student, MyUser
from .serializers import StudentSerializers, UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all() #type: ignore
    serializer_class = StudentSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]
    

class UserViewSet(viewsets.ModelViewSet):
        queryset = MyUser.objects.all()  #type: ignore
        http_method_names = ['get', 'post', 'patch', 'delete']
        serializer_class = UserSerializer
 
