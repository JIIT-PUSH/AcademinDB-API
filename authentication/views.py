from authentication.serializer import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from authentication.models import User
from authentication.cloudant import create_user_database

class Register(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['data']
        profile = {
            "username": serializer.validated_data['username'],
            "name": serializer.validated_data['name'],
            "user_type": serializer.validated_data['user_type'],
            "phoneNumber": serializer.validated_data['phone'],
            "emailAddress": serializer.validated_data['email'],
        }
        profile.update(data)
        create_user_database(profile)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

