from rest_framework import serializers

from reels.models import Reel


class ReelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def save(self, **kwargs):
        reel = self.validated_data.get('reel', None)
        title = self.validated_data.get('title')
        description = self.validated_data.get('description')

        if not reel:
            raise serializers.ValidationError('Reel not found.')

        if not title:
            raise serializers.ValidationError('Title Reel not found.')


        user = kwargs.get('user', None)
        if not user:
            raise serializers.ValidationError('User not provided.')

        Reel.objects.create(
            reel=reel,
            user=user,
            title=title,
            description=description
        )

class ReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = '__all__'

