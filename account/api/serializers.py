from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from .. import models

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    )

# User = get_user_model()


class StuCreateSerializer(ModelSerializer):
    email = serializers.EmailField(label='Email')
    sapid = serializers.IntegerField(label='Sap id')
    email2 = serializers.EmailField(label='Confirm email', write_only=True)
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, write_only=True)

    class Meta:
        # model = User
        model = models.CustomUser
        fields = ['username', 'sapid', 'email', 'email2', 'password']
        extra_kwargs = {"password": {"write_only": True},
                        }

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        user_queryset = models.CustomUser.objects.filter(email=email2)
        if user_queryset.exists():
            raise ValidationError("This email address is registered.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        sapid = validated_data['sapid']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = models.CustomUser(
            username=username,
            sapid=sapid,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class TeacherCreateSerializer(ModelSerializer):
    email = serializers.EmailField(label='Email')
    dept = serializers.CharField(label='Department')
    email2 = serializers.EmailField(label='Confirm email', write_only=True)
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, write_only=True)

    class Meta:
        # model = User
        model = models.CustomUser
        fields = ['username', 'dept', 'email', 'email2', 'password']
        extra_kwargs = {"password": {"write_only": True},
                        }

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        user_queryset = models.CustomUser.objects.filter(email=email2)
        if user_queryset.exists():
            raise ValidationError("This email address is registered.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        dept = validated_data['dept']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = models.CustomUser(
            username=username,
            dept=dept,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):

    token = serializers.CharField(allow_blank=True, read_only=True)
    field_value = serializers.CharField(required=False, allow_blank=True, label='SapId/Email', write_only=True)
    # sapid = serializers.IntegerField(required=False, allow_null=True)
    # email = serializers.EmailField(label='Email', required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password',
                                            'placeholder': 'Type your password to get hacked ;)'},
                                     write_only=True)

    class Meta:
        # model = User
        model = models.CustomUser
        # fields = ['username', 'sapid', 'email', 'password', 'token']
        fields = ['field_value', 'password', 'token']
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        # email = data.get("email", None)
        field_value = data.get("field_value", None)
        # sapid = data.get("sapid", None)
        password = data["password"]
        # if not email and not username and not sapid:
        #     raise ValidationError("Username or email or sapid is required")

        # if email and username and sapid:
        #     raise ValidationError('Enter a single field')

        # user = models.CustomUser.objects.filter(
        #         Q(email=email) | Q(username=username) | Q(sapid=sapid)
        #     ).distinct()
        # user = models.CustomUser.objects.filter(
        #         Q(username=username) | Q(sapid=sapid)
        #     ).distinct
        # user = user.exclude(email__isnull=True).exclude(email__iexact='')

        if '@' in field_value:
            user = models.CustomUser.objects.filter(email__iexact=field_value).first()
        elif field_value.isdigit():
            user = models.CustomUser.objects.filter(sapid=field_value).first()
        else:
            # user = models.CustomUser.objects.filter(username__iexact=field_value).first()
            raise ValidationError('Incorrect field value')

        if not user:
            raise serializers.ValidationError("User does not exist")

        # if user.exists() and user.count() == 1:
        #     user_obj = user.first()
        # else:
        #     raise ValidationError("This username or email is not valid")

        user_obj = user

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials")
        data["token"] = "some random token"
        return data
