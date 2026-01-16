from rest_framework import serializers # type: ignore
from .models import Student, MyUser, Assessment, TermReport

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["user_id", "password", "last_login", "email", "is_staff", "is_active", "username", "first_name", "last_name", "date_joined", "is_principal"]
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(
            password = password,
            **validated_data
        )
        return user
class AssessmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Assessment
        fields = ['subject_name', 'ca1_score', 'ca2_score', 
                  'ca3_score', 'exam_score', 'total_score', 'grade', 'remark']

class TermReportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = TermReport
        fields = ['report_id', 'student_name', 'session', 'term','average_score', 'position_in_class', 'assessments',                  'class_teacher_comment', 'principal_comment']
    
    def get_assessments(self, obj):
        assessments = obj.get_all_assessments()
        return AssessmentSerializer(assessments, many=True).data