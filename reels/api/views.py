from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reels.api.serializers import ReelCreateSerializer, ReelSerializer
from reels.models import Reel, Like, Comment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reels_view(request):
    response = {}
    serializer = ReelCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        response['message'] = "Your Reel Added"
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reels_view(request):
    reels = Reel.objects.all()
    serializer = ReelSerializer(reels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def del_reels_view(request, pk):
    try:
        reel = Reel.objects.get(id=pk, user=request.user)
        reel.delete()
        return Response({"message": "Reel deleted successfully."}, status=status.HTTP_200_OK)
    except Reel.DoesNotExist:
        return Response({"error": "Reel not found or you are not authorized to delete this reel."},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_likes_view(request, pk):
    try:
        reel = Reel.objects.filter(id=pk).first()
        user = request.user
        liked = Like.objects.filter(reel=reel, user=user).exists()
        if liked:
            like = Like.objects.filter(reel=reel, user=user)
            like.delete()
            return Response({"message": "Reel un liked."}, status=status.HTTP_201_CREATED)
        else:
            like = Like.objects.create(
                reel=reel,
                user=user
            )
            like.save()
            return Response({"message": "Reel liked."}, status=status.HTTP_201_CREATED)
    except Reel.DoesNotExist:
        return Response({"error": "Reel not found or you not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment_view(request, pk):
    try:
        reel = Reel.objects.filter(id=pk).first()
        user = request.user
        data = request.data
        text = data.get('text')
        comment = Comment.objects.create(
            reel=reel,
            user=user,
            text=text
        )
        comment.save()
        return Response({"message": "Reel Commented"}, status=status.HTTP_201_CREATED)
    except Reel.DoesNotExist:
        return Response({"error": "Reel not found or you not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def del_comment_view(request, pk):
    try:
        comment = Comment.objects.get(id=pk, user=request.user)
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found or you are not authorized to delete this comment."},
                        status=status.HTTP_404_NOT_FOUND)