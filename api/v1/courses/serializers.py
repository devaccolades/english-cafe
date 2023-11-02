from rest_framework import serializers
from courses.models import *
from general.encryptions import decrypt 
from django.http import FileResponse


class StudentDayListSerializer(serializers.ModelSerializer):
    student_day_pk = serializers.SerializerMethodField()
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
            'student_day_pk',
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
    
    def get_student_day_pk(self, instance):
        student = self.context['student']
        if (student_day := StudentDay.objects.filter(day=instance, student=student)).exists():
            student_day = student_day.latest("date_added")

            student_day_pk = student_day.id
            return student_day_pk
        else:
            return None



class DailyAudioTopicSerializer(serializers.ModelSerializer):
    is_processed = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DailyAudioTopic
        fields = (
            'id',
            'audio',
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
            "alt",
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
    video = serializers.SerializerMethodField()
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

    
    def get_video(self, instance):
        request = self.context['request']
        if instance.video:
            video_url =  request.build_absolute_uri(instance.video.url)
            with open(video_url, 'rb') as video_file:
                video_link = FileResponse(video_file)
                video_link['Content-Type'] = 'video/mp4'
                return video_link
        else:
            return None
    
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


class AdminDayListSerializer(serializers.ModelSerializer):
    programme = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = (
            'id',
            'programme',
            'day_number',
            'no_of_contents'
        )
    
    def get_programme(self, instance):
        if instance.programme:
            return instance.programme.name
        else:
            return None
        

class AddDaysSerializer(serializers.Serializer):
    days = serializers.CharField()


class ProgrammeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = (
            'id',
            'name',
            'duration',
            'description',
            'order_id'
        )


class AddProgrammeSerializer(serializers.Serializer):
    name = serializers.CharField()
    duration = serializers.CharField()
    description = serializers.CharField()
    order_id = serializers.CharField()


class AddDaySerializer(serializers.Serializer):
    day_number = serializers.CharField()


class AddNumberOfContentSerializer(serializers.Serializer):
    number_of_content = serializers.CharField()


class DailyAdminAudioTopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DailyAudioTopic
        fields = (
            'id',
            'audio',
            "order_id",
        )
    
    
    
    
class DailyAdminImageTopicSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = DailyImageTopic
        fields = (
            "id",
            "daily_image",
            "order_id",
        )

class DailyAdminVideoTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyVideoTopic
        fields = (
            'id',
            'video',
            "order_id",
        )

    
class DailyAdminTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyTextTopic
        fields = (
            'id',
            'daily_text',
            "order_id",
        )

    

    


    