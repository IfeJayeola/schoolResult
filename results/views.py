from django.shortcuts import render # type: ignore
from .models import Student, MyUser, Assessment, TermReport, AcademicSession, Subject, ClassRoom 
from .serializers import StudentSerializers, UserSerializer, TermReportSerializer, AssessmentSerializer, AcademicSessionSerializer, SubjectSerializer, ClassRoomSerializer
from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAuthenticated, is_principal # type: ignore

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
    permission_classes = [IsAuthenticated]
 

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()  #type: ignore
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
 

class TermReportViewSet(viewsets.ModelViewSet):
    queryset = TermReport.objects.all()  #type: ignore
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = TermReportSerializer
    permission_classes = [IsAuthenticated]
 

class AcademicSessionViewSet(viewsets.ModelViewSet):
    queryset = AcademicSession.objects.all()  #type: ignore
    http_method_names = ['get', 'post']
    serializer_class = AcademicSessionSerializer
    permission_classes = [IsAuthenticated]
 

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()  #type: ignore
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]
 

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()  #type: ignore
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
 

