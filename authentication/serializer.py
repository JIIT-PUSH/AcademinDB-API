from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'data', 'user_type', 'email', 'password', 'token']
        read_only_fields = ('token',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    error = serializers.BooleanField(read_only=True)
    message = serializers.CharField(max_length=120, read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    schoolcode = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('A Username is required to log in.')
        if password is None:
            raise serializers.ValidationError('A Password is required to log in.')
        
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid Password')
        else:
            raise serializers.ValidationError('Username not Found. Consider Registring First')
        
        if user.user_type == 'teacher' or user.user_type == 'student':
            return {
                'error': False,
                'message': 'Login Successful',
                'username':user.username,
                'token':user.token,
                'schoolcode':user.data['schoolcode']
                }

        elif user.user_type == 'school':
            return {
                'error': False,
                'message': 'Login Successful',
                'username':user.username,
                'token':user.token
                } 
                
class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'data', 'email']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.email = validated_data.get('email',instance.email)
        instance.data = validated_data.get('data',instance.data)
        return instance 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self,value):
        validate_password(value)
        return value