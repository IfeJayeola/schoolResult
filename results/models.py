import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import uuid
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


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
class Student_class(models.TextChoices):
    JS1 = 'js1', 'Js1' 
    JS2 = 'js2', 'Js2' 
    JS3 = 'js3', 'Js3' 
    SS1 = 'ss1', 'Ss1' 
    SS2 = 'ss2', 'Ss2' 
    SS3 = 'ss3', 'Ss3'

class Gender_select(models.TextChoices):
    Male = 'M', 'Male'
    Female = 'F', 'Female'



class MyUser(AbstractUser):
    user_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
        )
    username = models.CharField(unique = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    date_joined = models.DateTimeField(auto_now_add= True)
    is_principal = models.BooleanField(default=False) #type: ignore

    objects = MyUserManager()
    

    USERNAME_FIELD = 'username'
#    REQUIRED_FIELDS =

    
    

class Student(models.Model):
    last_name = models.CharField(
        max_length = 20,
        null = False
    )
    first_name = models.CharField(
        max_length = 20,
        null = False
    )
    middle_name = models.CharField(
        max_length = 20
    )
    student_class = models.CharField(
        max_length = 5,
        choices = Student_class.choices
    )


class Assessment(models.Model):
    """
    Stores CA and exam scores for each student's subject enrollment.
    One assessment per subject registration (student + subject + session).
    """
    
    assessment_id = models.AutoField(primary_key=True)
    
    # Link to subject registration (contains student, subject, session)
    registration = models.OneToOneField(
        'SubjectRegistration',
        on_delete=models.CASCADE,
        related_name='assessment',
        help_text="Subject registration this assessment belongs to"
    )
    
    # Continuous Assessment scores (max 10 each)
    ca1_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(10.00)
        ],
        help_text="First Continuous Assessment (max 10)"
    )
    
    ca2_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(0.00), #type: ignore
            MaxValueValidator(10.00) #type: ignore
        ],
        help_text="Second Continuous Assessment (max 10)"
    )
    
    ca3_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(0.00), #type: ignore
            MaxValueValidator(10.00) #type: ignore
        ],
        help_text="Third Continuous Assessment (max 10)"
    )
    
    # Exam score (max 70)
    exam_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(70.00)
        ],
        help_text="Examination score (max 70)"
    )
    
    # Teacher's remarks on student performance
    teacher_remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Teacher's comments on student's performance"
    )
    
    # Track who recorded the scores
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assessments_recorded',
        help_text="User who recorded these scores"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessment'
        ordering = ['-created_at']
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'
        indexes = [
            models.Index(fields=['registration']),
            models.Index(fields=['recorded_by']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Assessment for {self.registration}"
    
    # Computed properties (not stored in database)
    @property
    def total_score(self):
        """Calculate total score (CA1 + CA2 + CA3 + Exam)"""
        return float(self.ca1_score + self.ca2_score + self.ca3_score + self.exam_score)
    
    @property
    def grade_info(self):
        """
        Get grade letter, grade point, and remark based on total score.
        Returns dict with: letter, point, remark
        """
        total = self.total_score
        
        # Nigerian WAEC grading scale
        if total >= 75:
            return {'letter': 'A1', 'point': 5.0, 'remark': 'Excellent'}
        elif total >= 70:
            return {'letter': 'B2', 'point': 4.5, 'remark': 'Very Good'}
        elif total >= 65:
            return {'letter': 'B3', 'point': 4.0, 'remark': 'Good'}
        elif total >= 60:
            return {'letter': 'C4', 'point': 3.5, 'remark': 'Credit'}
        elif total >= 55:
            return {'letter': 'C5', 'point': 3.0, 'remark': 'Credit'}
        elif total >= 50:
            return {'letter': 'C6', 'point': 2.5, 'remark': 'Credit'}
        elif total >= 45:
            return {'letter': 'D7', 'point': 2.0, 'remark': 'Pass'}
        elif total >= 40:
            return {'letter': 'E8', 'point': 1.5, 'remark': 'Pass'}
        else:
            return {'letter': 'F9', 'point': 0.0, 'remark': 'Fail'}
    
    @property
    def grade_letter(self):
        """Get grade letter only (A1, B2, etc.)"""
        return self.grade_info['letter']
    
    @property
    def grade_point(self):
        """Get grade point only (5.0, 4.5, etc.)"""
        return self.grade_info['point']
    
    @property
    def grade_remark(self):
        """Get grade remark only (Excellent, Pass, Fail)"""
        return self.grade_info['remark']
    
    @property
    def passed(self):
        """Check if student passed (score >= 40)"""
        return self.total_score >= 40
    
    @property
    def student(self):
        """Get student from registration"""
        return self.registration.student
    
    @property
    def subject(self):
        """Get subject from registration"""
        return self.registration.subject
    
    @property
    def session(self):
        """Get academic session from registration"""
        return self.registration.session
    
    def clean(self):
        """Validate scores before saving"""
        from django.core.exceptions import ValidationError
        
        # Ensure scores are within valid ranges
        if self.ca1_score < 0 or self.ca1_score > 10:
            raise ValidationError({'ca1_score': 'CA1 score must be between 0 and 10'})
        
        if self.ca2_score < 0 or self.ca2_score > 10:
            raise ValidationError({'ca2_score': 'CA2 score must be between 0 and 10'})
        
        if self.ca3_score < 0 or self.ca3_score > 10:
            raise ValidationError({'ca3_score': 'CA3 score must be between 0 and 10'})
        
        if self.exam_score < 0 or self.exam_score > 70:
            raise ValidationError({'exam_score': 'Exam score must be between 0 and 70'})
    
    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.full_clean()
        super().save(*args, **kwargs)
