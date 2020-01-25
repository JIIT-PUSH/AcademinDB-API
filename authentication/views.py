from authentication.serializer import RegisterSerializer, LoginSerializer, UpdateProfileSerializer, ChangePasswordSerializer
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
    queryset = User.objects.all()

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
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateProfileSerializer
    queryset = User.objects.all()

    def get_object(self, pk):
        try:
            return User.objects.get(pk='username')
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdateProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdateProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def get_object(self):
    #     username = self.kwargs["username"]
    #     name = self.kwargs["name"]
    #     phone = self.kwargs["phone"]
    #     email = self.kwargs["email"]
    #     data = self.kwargs["data"]
    #     obj = get_object_or_404(User, username=username)
    #     return obj

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

class ChangePassword(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, UserIsOwnerOrReadOnly)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)