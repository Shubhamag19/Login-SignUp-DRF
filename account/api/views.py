from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    )
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly,)

# from posts.api.permissions import IsOwnerOrReadOnly

User = get_user_model()

from .serializers import (
    StuCreateSerializer,
    TeacherCreateSerializer,
    UserLoginSerializer,
    )


class StuCreateAPIView(CreateAPIView):

    serializer_class = StuCreateSerializer
    queryset = User.objects.all()


class TeachCreateAPIView(CreateAPIView):

    serializer_class = TeacherCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):

        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)