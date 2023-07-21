from rest_framework import serializers
from courses.models import *



class DailyAudioTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAudioTopic
        fields = (
            'id',
            'audio',
            'text',
            "order_id",
        )


class DailyImageTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyImageTopic
        fields = (
            "id",
            "daily_image",
            "order_id",

        )


class DailyVideoTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyVideoTopic
        fields = (
            'id',
            'video',
            "order_id",

        )


class DailyTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTextTopic
        fields = (
            'id',
            'daily_text',
            "order_id",

        )