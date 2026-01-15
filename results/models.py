import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator



class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)

# Create your models here
class StudentClass(models.TextChoices):
    JS1 = 'js1', 'Js1' 
    JS2 = 'js2', 'Js2' 
    JS3 = 'js3', 'Js3' 
    SS1 = 'ss1', 'Ss1' 
    SS2 = 'ss2', 'Ss2' 
    SS3 = 'ss3', 'Ss3'


class GenderSelect(models.TextChoices):
    Male = 'M', 'Male'
    Female = 'F', 'Female'


class Term(models.TextChoices):
    FIRST = 'FIRST', 'First Term'
    SECOND = 'SECOND', 'Second Term'
    THIRD = 'THIRD', 'Third Term'


class MyUser(AbstractUser):
    user_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
        )
    username = models.CharField(max_length=150, unique = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField(unique=True, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add= True)
    is_principal = models.BooleanField(default=False) 
    is_teacher = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
#    REQUIRED_FIELDS =

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    

    
class AcademicSession(models.Model):
    sesson_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 20, null = False)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = 'academic_sessions'
        ordering = ['-start_date']

    def __str__(self):
        return self.name
    

class ClassRoom(models.Model):
    class_id =  models.AutoField(primary_keyy = True)
    class_level = models.CharField(max_length=3, choices=StudentClass.choices)
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='classes')
    class_teacher = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes_as_teacher'
    )

    class Meta:
        db_table = 'classrooms'
        unique_together = ['class_level', 'session']

    def __str__(self):
        return f"{self.class_level} ({self.session})"    


class Subject(models.Model):
    subject_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(
        max_length = 20,
        null = False
    )
    middle_name = models.CharField(
        max_length = 20,
        null = True
    )
    last_name = models.CharField(
        max_length = 20,
        null = False
    )
    gender = models.CharField(max_length=1, choices=GenderSelect.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    current_class = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    admission_date = models.DateField(null = False, blank = False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.admission_number} - {self.get_full_name()}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class Assessment(models.Model):
    #subject
    #session
    #student
    #class 
    assessment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assessments')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='assessments')
    term = models.CharField(max_length=10, choices=Term.choices)
    ca1_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.00,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(10.0)
        ],
    )
    ca2_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.00,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(10.0)
        ],
    )
    ca3_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.00,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(10.0)
        ],
    )
    exam_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.00,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(70.00)
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assessments'
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'session', 'term']

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.get_term_display()}, {self.session})"    

    @property
    def total_score(self):
        return self.ca1_score + self.ca2_score + self.ca3_score + self.exam_score

    @property
    def grade(self):
        total = self.total_score
        if total >= 70:
            return 'A'
        elif total >= 60:
            return 'B'
        elif total >= 50:
            return 'C'
        elif total >= 45:
            return 'D'
        elif total >= 40:
            return 'E'
        else:
            return 'F'

    @property
    def remark(self):
        grade_remarks = {
            'A': 'Excellent',
            'B': 'Very Good',
            'C': 'Good',
            'D': 'Pass',
            'E': 'Poor',
            'F': 'Fail'
        }
        return grade_remarks.get(self.grade, 'N/A')    
    

class TermReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='reports')
    term = models.CharField(max_length=10, choices=Term.choices)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='reports')
