from authentication.serializer import RegisterSerializer, LoginSerializer, UpdateProfileSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from authentication.models import User
from authentication.cloudant import create_user_database
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions

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

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class Update(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, UserIsOwnerOrReadOnly)
    serializer_class = UpdateProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset = User.objects.all()

    def get_object(self):
        username = self.kwargs["username"]
        name = self.kwargs["name"]
        phone = self.kwargs["phone"]
        email = self.kwargs["email"]
        data = self.kwargs["data"]
        obj = get_object_or_404(User, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)