import requests
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from django.db import transaction

from general.decorators import group_required
from general.functions import generate_serializer_errors, loginUser, get_first_letters, get_auto_id, create_student_day_for_new_student, create_student_first_topic_for_a_new_student
from general.encryptions import decrypt, encrypt
from api.v1.accounts.serializers import *
from accounts.models import *
from courses.models import Programme



@api_view(['POST'])
@permission_classes([AllowAny,])
def chief_profile_login(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = ChiefProfileLoginSerializer(data=request.data)
        if serialized_data.is_valid():
            username = request.data['username']
            password = request.data['password']
            if (chief_profile := ChiefProfile.objects.filter(username=username)).exists():
                chief_profile = chief_profile.latest('date_added')

                decrypted_password = decrypt(chief_profile.password)
                if decrypted_password == password:
                    access = loginUser(request, chief_profile.user)

                    transaction.commit()

                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "access" : access
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Incorrect"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Chief profile not exists"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['EnglishCafe'])
def create_student_profile(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateStudentProfileSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            phone = request.data["phone"]
            password = request.data["password"]
            programme_id = request.data["programme"]

            if (programme := Programme.objects.filter(pk=programme_id, is_deleted=False)).exists():
                programme = programme.latest('date_added')

                letters_of_student = get_first_letters(name)
                number = get_auto_id(StudentProfile)
                username = 'EC'+letters_of_student+str(number).zfill(2)

                if not StudentProfile.objects.filter(phone=phone).exists():
                    user = User.objects.create_user(
                            username=username,
                            password=make_password(password)
                        )
                    group_name = 'Student'
                    group, created = Group.objects.get_or_create(
                            name=group_name)
                    user.groups.add(group)

                    student_profile = StudentProfile.objects.create(
                        auto_id = number,
                        username = username,
                        user=user,
                        password = encrypt(password),
                        name = name,
                        phone = phone,
                        admission_number = username,
                        programmes = programme
                    )

                    student_data = {
                        "student_id" : student_profile.id,
                        "user_pk" : student_profile.user.id
                    }

                    create_student_day_for_new_student(student_data,programme)
                    create_student_first_topic_for_a_new_student(student_data, programme)

                    transaction.commit()

                    response_data = {
                        "StatusCode" : 6000,
                        "credentials" : {
                            "username" : username,
                            "password" : password
                        },
                        "data" : {
                            "title" : "Success",
                            "message" : "Student profile created successfully"
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Profile already exists"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Programme not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny,])
def login_student_profile(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = StudentProfileLoginSerializer(data=request.data)

        if serialized_data.is_valid():
            username = request.data['username']
            password = request.data['password']

            if (student_profile := StudentProfile.objects.filter(username=username)).exists():
                student_profile = student_profile.latest('date_added')

                decrypted_password = decrypt(student_profile.password)
                if decrypted_password == password:
                    access = loginUser(request, student_profile.user)

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "access" : access
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Incorrect password"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Student profile not exists"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 6001,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@group_required(['EnglishCafe'])
def programme_list(request):
    try:
        if (programmes := Programme.objects.filter(is_deleted=False)).exists():

            serialized_data = ProgrammeListSerializers(
                programmes,
                context = {
                    "request" : request
                },
                many=True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Programme not found" 
                }
            }
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as E:
        return Response({'app_data': 'something went wrong', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)
