from rest_framework import serializers
from .models import Student, MyUser

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
