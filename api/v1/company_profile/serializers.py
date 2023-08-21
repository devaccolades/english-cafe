from rest_framework import serializers
from company_profile.models import *


class AddAchievementsSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class AchievementListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Achievements
        fields = (
            'id',
            'title',
            'image',
            'description',
        )

    def get_image(self, instance):
        request = self.context['request']
        if instance.image:
            return request.build_absolute_uri(instance.image.url)
        else:
            return None
        

class AddTestimonialSerializer(serializers.Serializer):
    name = serializers.CharField()
    quote = serializers.CharField()
    image = serializers.FileField()
    rating_count = serializers.CharField()


class TestimonialListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Testimonials
        fields = (
            'id',
            'name',
            'quote',
            'rating_count',
            'image',
            'video',
        )

    def get_image(self, instance):
        request = self.context['request']
        if instance.image:
            return request.build_absolute_uri(instance.image.url)
        else:
            return None


    def get_video(self, instance):
        request = self.context['request']
        if instance.video:
            return request.build_absolute_uri(instance.video.url)
        else:
            return None
        
    
class AddOurTeamSerializer(serializers.Serializer):
    name = serializers.CharField()
    photo = serializers.FileField()
    designation = serializers.CharField()


class OurTeamListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = OurTeam
        fields = (
            'id',
            'name',
            'photo',
            'designation',

        )

    def get_photo(self, instance):
        request = self.context['request']
        if instance.photo:
            return request.build_absolute_uri(instance.photo.url)
        else:
            return None
        

class AddCareerSerializer(serializers.Serializer):
    designation = serializers.CharField()
    job_description = serializers.CharField()
    job_type = serializers.CharField()


class CareerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Career
        fields = (
            'id',
            'designation',
            'job_description',
            'job_type'
        )


class AddCareerEnquirySerializer(serializers.Serializer):
    job = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    cv = serializers.FileField()


class CareerEnquirySerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()

    class Meta:
        model = CareerEnquiry
        fields = (
            'id',
            'job',
            'name',
            'phone',
            'email',
            'cv',
        )

    def get_job(self,instance):
        if instance.job:
            return instance.job.designation
        else:
            return None
        
    def get_cv(self,instance):
        request = self.context['request']
        if instance.cv:
            return request.build_absolute_uri(instance.cv.url)
        else:
            return None
        
    
class EnquiryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enquiry
        fields = (
            'id',
            'name',
            'phone',
            'email',
            'message'
        )


class CreateEnquirySerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()
