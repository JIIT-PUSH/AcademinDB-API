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


    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'A Username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A Password is required to log in.'
            )
        usernameVerified = User.objects.get(username=username)
        if usernameVerified is none:
            raise serializers.ValidationError(
                'Username not found, please consider registration first'
        )

        if not User.check_password(password):
            raise serializers.ValidationError(
                'Password Invalid'
        )

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        return {
            'error': False,
            'message': 'Login Successful',
            'username':user.username,
            'token':user.token
        }

