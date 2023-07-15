from rest_framework import serializers


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