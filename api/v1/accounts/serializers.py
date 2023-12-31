from rest_framework import serializers
from courses.models import Programme
from accounts.models import StudentProfile
from general.encryptions import decrypt


class ChiefProfileLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateStudentProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField()
    programme = serializers.CharField()


class StudentProfileLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class StudentListSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()
    programmes = serializers.SerializerMethodField()
    programme_id = serializers.SerializerMethodField()
    programme_duration = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = (
            'id',
            'name',
            'username',
            'password',
            'phone',
            'programmes',
            'programme_id',
            'programme_duration',
        )

    def get_password(self, instance):
        if instance.password:
            decrypted_password = decrypt(instance.password)

            return decrypted_password
        else:
            return None
        
    def get_programmes(self, instance):
        if instance.programmes:
            return instance.programmes.name
        else:
            return 
        
    def get_programme_id(self, instance):
        if instance.programmes:
            return  instance.programmes.id
        else:
            return None
        
    def get_programme_duration(self, instance):
        if instance.programmes:
            return instance.programmes.duration
        else:
            return None
