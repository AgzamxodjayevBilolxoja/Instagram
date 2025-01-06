from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class RegisterFirstStageSerializer(serializers.Serializer):
    contact = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        contact = data.get('contact')
        password = data.get('password')
        full_name = data.get('full_name')
        username = data.get('username')

        email = contact if '@' in contact else False
        phone = contact if not '@' in contact else False

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This EMAIL already exists!')

        if phone and User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError('This PHONE NUMBER already exists!')

        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This USERNAME already exists!')

        user = {
            'email': email,
            'phone': phone,
            'password': password,
            'full_name': full_name,
            'username': username
        }

        data['user'] = user
        return data


class RegisterThirdStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'password', 'full_name', 'username', 'date_of_birth']

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        phone_number = self.validated_data.get('phone_number')
        password = self.validated_data.get('password')
        full_name = self.validated_data.get('full_name')
        username = self.validated_data.get('username')
        birthday = self.validated_data.get('birthday')

        user = User.objects.create_user(email=email, phone_number=phone_number, password=password, full_name=full_name,
                                 username=username, date_of_birth=birthday)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    login = serializers.CharField()

    def validate(self, data):
        password = data.get('password')
        login = data.get("login")

        user = authenticate(username=login, password=password)
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid login")

        return data

class UpdateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    gender = serializers.ChoiceField(choices=['male', 'female', 'undefined'], required=False)

    def validate(self, data):
        if not self.context.get('user'):
            raise serializers.ValidationError("User object is required in the context.")
        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.username = validated_data.get('username', instance.username)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance