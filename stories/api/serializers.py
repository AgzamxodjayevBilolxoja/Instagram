from rest_framework import serializers

from stories.models import Story


class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def save(self, **kwargs):
        story = self.validated_data.get('story', None)
        title = self.validated_data.get('title')
        description = self.validated_data.get('description')

        if not story:
            raise serializers.ValidationError('Story not found.')

        if not title:
            raise serializers.ValidationError('Title Story not found.')


        user = kwargs.get('user', None)
        if not user:
            raise serializers.ValidationError('User not provided.')

        Story.objects.create(
            story=story,
            user=user,
            title=title,
            description=description
        )

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
