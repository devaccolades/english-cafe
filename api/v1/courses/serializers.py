from rest_framework import serializers
from courses.models import *


class StudentDayListSerializer(serializers.ModelSerializer):
    programme = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = (
            'id',
            'programme',
            'day_number',
            'no_of_contents',
            'is_completed',
            'status',
        )
    
    def get_programme(self, instance):
        if instance.programme:
            return instance.programme.name
        else:
            return None
        
    def get_is_completed(self, instance):
        student = self.context['student']
        if (student_day := StudentDay.objects.filter(day=instance, student=student)).exists():
            student_day = student_day.latest("date_added")

            return student_day.is_completed
        else:
            return False
        
    def get_status(self, instance):
        student = self.context['student']
        if (student_day := StudentDay.objects.filter(day=instance, student=student)).exists():
            student_day = student_day.latest("date_added")

            return student_day.status
        else:
            return 'locked'


class DailyAudioTopicSerializer(serializers.ModelSerializer):
    is_processed = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DailyAudioTopic
        fields = (
            'id',
            'audio',
            'text',
            "order_id",
            "is_processed",
            "is_completed",
            "next_topic_id"
        )
    
    def get_is_processed(self, instance):
        student = self.context['student_id']
        if (student_audio_topic := StudentDailyAudioTopic.objects.filter(daily_audio_topic=instance.id, student_profile=student )).exists():
            student_audio_topic = student_audio_topic.latest("date_added")
            if student_audio_topic:
                return student_audio_topic.is_processed
            else:
                False
        else:
            return False
        
    def get_is_completed(self, instance):
        student = self.context['student_id']
        if (student_audio_topic := StudentDailyAudioTopic.objects.filter(daily_audio_topic=instance.id, student_profile=student)).exists():
            student_audio_topic = student_audio_topic.latest("date_added")
            if student_audio_topic:
                return student_audio_topic.is_completed
            else:
                False
        else:
            return False


class DailyImageTopicSerializer(serializers.ModelSerializer):
    is_processed = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DailyImageTopic
        fields = (
            "id",
            "daily_image",
            "order_id",
            "is_processed",
            "is_completed",
            "next_topic_id"


        )
    
    def get_is_processed(self, instance):
        student = self.context['student_id']
        if (student_image_topic := StudentDailyImageTopic.objects.filter(daily_image_topic=instance.id,  student_profile=student)).exists():
            student_image_topic = student_image_topic.latest("date_added")
            if student_image_topic:
                return student_image_topic.is_processed
            else:
                False
        else:
            return False
        
    def get_is_completed(self, instance):
        student = self.context['student_id']
        if (student_image_topic := StudentDailyImageTopic.objects.filter(daily_image_topic=instance.id, student_profile=student)).exists():
            student_image_topic = student_image_topic.latest("date_added")
            if student_image_topic:
                return student_image_topic.is_completed
            else:
                False
        else:
            return False


class DailyVideoTopicSerializer(serializers.ModelSerializer):
    is_processed = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DailyVideoTopic
        fields = (
            'id',
            'video',
            "order_id",
            "is_processed",
            "is_completed",
            "next_topic_id"

        )
    
    def get_is_processed(self, instance):
        student = self.context['student_id']
        if (student_video_topic := StudentDailyVideoTopic.objects.filter(daily_video_topic=instance.id, student_profile=student)).exists():
            student_video_topic = student_video_topic.latest("date_added")
            if student_video_topic:
                return student_video_topic.is_processed
            else:
                False
        else:
            return False
        
    def get_is_completed(self, instance):
        student = self.context['student_id']
        if (student_video_topic := StudentDailyVideoTopic.objects.filter(daily_video_topic=instance.id, student_profile=student)).exists():
            student_video_topic = student_video_topic.latest("date_added")
            if student_video_topic:
                return student_video_topic.is_completed
            else:
                False
        else:
            return False


class DailyTextSerializer(serializers.ModelSerializer):
    is_processed = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DailyTextTopic
        fields = (
            'id',
            'daily_text',
            "order_id",
            "is_processed",
            "is_completed",
            "next_topic_id"


        )

    def get_is_processed(self, instance):
        student = self.context['student_id']
        if (student_text_topic := StudentDailyTextTopic.objects.filter(daily_text_topic=instance.id, student_profile=student)).exists():
            student_text_topic = student_text_topic.latest("date_added")
            if student_text_topic:
                return student_text_topic.is_processed
            else:
                False
        else:
            return False
        
    def get_is_completed(self, instance):
        student = self.context['student_id']
        if (student_text_topic := StudentDailyTextTopic.objects.filter(daily_text_topic=instance.id, student_profile=student)).exists():
            student_text_topic = student_text_topic.latest("date_added")
            if student_text_topic:
                return student_text_topic.is_completed
            else:
                False
        else:
            return False

class DailyTopicCompleteSerializer(serializers.Serializer):
    topic_type = serializers.CharField()


class AddDailyTopicSerializer(serializers.Serializer):
    day = serializers.CharField()
    topic_type = serializers.CharField()
    order_id = serializers.CharField()