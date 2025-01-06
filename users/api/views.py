import random
from urllib.robotparser import RequestRate

from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.api.serializers import RegisterFirstStageSerializer, RegisterThirdStageSerializer, LoginSerializer, \
    UpdateUserSerializer
from rest_framework.authtoken.models import Token

from users.models import User, Subscribe


@api_view(['POST'])
@permission_classes([AllowAny])
def register_stage1_view(request):
    response = {}
    serializer = RegisterFirstStageSerializer(data=request.data)
    if serializer.is_valid():
        response['message'] = 'You Passed The First Stage'
        request.session['user'] = serializer.validated_data['user']
        request.session['has_visited_register_stage_1'] = True
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_stage2_view(request):
    if 'has_visited_register_stage_1' in request.session:
        response = {}
        user_data = request.session.get('user', None)

        if not user_data:
            return Response({"error": "User data is missing."}, status=status.HTTP_400_BAD_REQUEST)

        user_data['birthday'] = request.data.get('birthday')
        random_number = random.randint(100000, 999999)
        response['message'] = 'You Passed The Second Stage'
        response['verification_code'] = random_number
        request.session['code'] = random_number
        request.session['user'] = user_data
        request.session['has_visited_register_stage_1'] = False
        request.session['has_visited_register_stage_2'] = True
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You must first access the path 127.0.0.1:8000/user/register1/'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_stage3_view(request):
    if 'has_visited_register_stage_2' in request.session:
        response = {}
        user_data = request.session.get('user', None)

        if not user_data:
            return Response({"error": "User data is missing."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterThirdStageSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            token, create = Token.objects.get_or_create(user=user)
            response['message'] = 'SuccessFully Register!'
            response['token'] = token.key
            request.session['has_visited_register_stage_2'] = False
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You must first access the path 127.0.0.1:8000/user/register2/'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    response = {}
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data.get('user')
        response['token'] = user.auth_token.key
        return Response(response, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    user = request.user
    serializer = UpdateUserSerializer(data=request.data, context={'user': user})
    if serializer.is_valid():
        serializer.update(user, serializer.validated_data)
        return Response({"message": "User Updated."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_view(request):
    user = request.user
    token = Token.objects.filter(user=user).first()
    if token:
        token.delete()
    user.delete()
    return Response({"message": "User successfully deleted."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_view(request, pk):
    user1 = User.objects.filter(id=pk).first()
    if not user1:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user2 = request.user
    subscribe, created = Subscribe.objects.get_or_create(user1=user1, user2=user2)

    if not created:
        subscribe.delete()
        return Response({"message": "Subscription cancelled"}, status=status.HTTP_200_OK)

    return Response({"message": "You subscribed successfully"}, status=status.HTTP_201_CREATED)
