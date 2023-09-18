from rest_framework import serializers
from company_profile.models import *


class AddAchievementsSerializer(serializers.Serializer):
    title = serializers.CharField()


class AchievementListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Achievements
        fields = (
            'id',
            'title',
            'image',
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
    image = serializers.FileField(required=False)
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
    department = serializers.CharField()
    head = serializers.CharField()

class OurTeamDepartmentSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'team_members'
        )

    def get_team_members(self, instance):
        request = self.context["request"]
        if (our_team := OurTeam.objects.filter(department=instance.id, is_deleted=False)).exists():
            our_team = our_team.order_by("-head")
            serialized_data = OurTeamListSerializer(
                our_team,
                context = {
                    "request" : request
                },
                many=True 
            ).data

            return serialized_data
        else:
            return None


class OurTeamListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = OurTeam
        fields = (
            'id',
            'name',
            'photo',
            'designation',
            'department',
            'head'
        )

    def get_photo(self, instance):
        request = self.context['request']
        if instance.photo:
            return request.build_absolute_uri(instance.photo.url)
        else:
            return None
        
    
    def get_department(self, instance):
        if instance.department:
            return instance.department.name
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


class CompanyCountListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyCount
        fields = (
            'id',
            'successfull_students',
            'languages_trainee',
            'awards_won',
            'courses'
        )


class AddCompanyCountSerializer(serializers.Serializer):
    successfull_students = serializers.IntegerField()
    languages_trainee = serializers.IntegerField()
    awards_won = serializers.IntegerField()
    courses = serializers.IntegerField()


class ViewDepartMentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            'id',
            'name'
        )


class AddGallerySerializer(serializers.Serializer):
    type = serializers.CharField()


class ViewGalleryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = (
            'id',
            'type',
            'file',
        )
        

class ViewGalleryYoutubeLinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = (
            'id',
            'type',
            'file_link'
        )

