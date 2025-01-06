from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from stories.api.serializers import StorySerializer, StoryCreateSerializer
from stories.models import Story

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stories_view(request):
    response = {}
    serializer = StoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        response['message'] = "Your Story Added"
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stories_view(request):
    stories = Story.objects.all()
    serializer = StorySerializer(stories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def del_stories_view(request, pk):
    try:
        story = Story.objects.get(id=pk, user=request.user)
        story.delete()
        return Response({"message": "Story deleted successfully."}, status=status.HTTP_200_OK)
    except Story.DoesNotExist:
        return Response({"error": "Story not found or you are not authorized to delete this story."},
                        status=status.HTTP_404_NOT_FOUND)
