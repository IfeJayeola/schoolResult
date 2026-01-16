from rest_framework import serializers # type: ignore
from .models import Student, MyUser, Assessment, TermReport, ClassRoom, Subject, AcademicSession

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
                  'ca3_score', 'exam_score', 'total_score', 'grade', 'remark', 'student', 'session', 'term', 'subject']

class TermReportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_admission_number = serializers.CharField(source='student.admission_number', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    assessments = serializers.SerializerMethodField()
    
    class Meta:
        model = TermReport
        fields = ['report_id', 'student_name', 'session', 'term','average_score', 'position_in_class', 'session_name', 'student_admission_number', 'classroom_name', 'assessments']
    
    def get_assessments(self, obj):
        assessments = obj.get_all_assessments()
        return AssessmentSerializer(assessments, many=True).data
    

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = [ 'sesson_id', 'name', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['session_id']


class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = [
            'subject_id', 'name',  'applicable_classes'
        ]
        read_only_fields = ['subject_id']        


class ClassRoomSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)        
    student_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ClassRoom
        fields = [ 'class_id', 'class_level',  'session', 'session_name', 'class_teacher', 'student_count']
        read_only_fields = ['class_id']