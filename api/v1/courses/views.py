import traceback

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from general.decorators import group_required
from general.functions import generate_serializer_errors, get_auto_id
from courses.models import *
from accounts.models import StudentProfile
from api.v1.courses.serializers import *
from api.v1.courses.functions import assign_next_topic

@api_view(['GET'])
@group_required(['Student'])
def get_total_days(request):
    try:
        transaction.set_autocommit(False)
        user = request.user
        if (student := StudentProfile.objects.filter(user=user, is_deleted=False)).exists():
            student = student.latest("date_added")
            programme = student.programmes

            if (days := Day.objects.filter(programme=programme, is_deleted=False)).order_by('day_number').exists():

                serialized_data = StudentDayListSerializer(
                    days,
                    context = {
                        "request" : request,
                        "student" : student,
                    },
                    many=True
                ).data

                transaction.commit()

                response_data = {
                    "StatusCode" : 6000,
                    "data" : serialized_data, 
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Day not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Student not found"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@group_required(['Student'])
def get_daily_topics(request, pk):
    try:
        user =request.user
        if (student := StudentProfile.objects.filter(user=user, is_deleted=False)).exists():
            student = student.latest("date_added")

            if (student_day := StudentDay.objects.filter(day=pk, is_deleted=False)).exists():
                student_day = student_day.latest("id")
                day = student_day.day

                number_of_contents_in_a_day = student_day.day.no_of_contents

                topics =[]
                temp_data = []

                for i in range(int(number_of_contents_in_a_day)):

                    if (daily_audio_topics := DailyAudioTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                        daily_audio_topic_object = daily_audio_topics.latest("date_added")
                        if not temp_data:
                            temp_data.append(daily_audio_topic_object)
                        else:
                            temp_data[-1].next_topic_id = daily_audio_topic_object.id
                            temp_data[-1].save()
                            temp_data.append(daily_audio_topic_object)

                        audio_serialized_data = DailyAudioTopicSerializer(
                            daily_audio_topics,
                            context = {
                                "request" : request,
                                "student_id" : student,
                            },
                            many=True
                        ).data
                        audio_serialized_data[0]['type'] = "audio"
                        topics.append(audio_serialized_data[0])
                    else:
                        pass

                    if (daily_video_topics := DailyVideoTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                        daily_video_topics_object = daily_video_topics.latest("date_added")

                        if not temp_data:
                            temp_data.append(daily_video_topics_object)
                        else:
                            temp_data[-1].next_topic_id = daily_video_topics_object.id
                            temp_data[-1].save()
                            temp_data.append(daily_video_topics_object)

                        video_serialized_data = DailyVideoTopicSerializer(
                            daily_video_topics,
                            context = {
                                "request" : request,
                                "student_id" : student,
                            },
                            many=True
                        ).data

                        video_serialized_data[0]["type"] = "video"
                        topics.append(video_serialized_data[0])
                    else:
                        pass

                    if (daily_image_topic := DailyImageTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                        daily_image_topic_objects = daily_image_topic.latest("date_added")

                        if not temp_data:
                            temp_data.append(daily_image_topic_objects)
                        else:
                            temp_data[-1].next_topic_id = daily_image_topic_objects.id
                            temp_data[-1].save()
                            temp_data.append(daily_image_topic_objects)

                        image_serialized_data = DailyImageTopicSerializer(
                            daily_image_topic,
                            context = {
                                "request" : request,
                                "student_id" : student,
                            },
                            many=True
                        ).data

                        image_serialized_data[0]["type"] = "image"
                        topics.append(image_serialized_data[0])
                    else:
                        pass


                    if (daily_text_topic := DailyTextTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                        daily_text_topic_object = daily_text_topic.latest("date_added")

                        if not temp_data:
                            temp_data.append(daily_text_topic_object)
                        else:
                            temp_data[-1].next_topic_id = daily_text_topic_object.id
                            temp_data[-1].save()
                            temp_data.append(daily_text_topic_object)

                        text_serialized_data = DailyTextSerializer(
                            daily_text_topic,
                            context = {
                                "request" : request,
                                "student_id" : student,
                            },
                            many=True
                        ).data

                        text_serialized_data[0]["type"] = "text"
                        topics.append(text_serialized_data[0])

                response_data = {
                    "StatusCode" : 6000,
                    "data" : topics
                }
                
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Day not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Student not found"
                }
            }
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as E:
        return Response({'app_data': 'something went wrong', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@group_required(['Student'])
def daily_topic_complete(request, pk):
    try:
        transaction.set_autocommit(False)
        user = request.user

        if (student_profile := StudentProfile.objects.filter(user=user)).exists():
            student_profile = student_profile.latest("date_added")

            if (audio_topic := DailyAudioTopic.objects.filter(pk=pk)).exists():
                audio_topic = audio_topic.latest("date_added")
                next_topic_id = audio_topic.next_topic_id

                if not StudentDailyAudioTopic.objects.filter(daily_audio_topic=audio_topic, student_profile=student_profile).exists():
                    print("if not function ok")
                    student_audio_topic = StudentDailyAudioTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyAudioTopic),
                        daily_audio_topic = audio_topic,
                        student_profile = student_profile,
                        is_completed = True
                    )

                    if student_audio_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Student daily audio completed successfully"
                        }
                    }

                elif (student_daily_audio_topic := StudentDailyAudioTopic.objects.filter(daily_audio_topic=audio_topic, student_profile=student_profile, is_completed=False)).exists():
                    print("come to elif function")
                    student_daily_audio_topic = student_daily_audio_topic.latest("date_added")
                    student_daily_audio_topic.is_completed = True
                    student_daily_audio_topic.save()
                    
                    if student_daily_audio_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : f"Student {audio_topic.day} video topic already exists"
                        }
                    }

            elif (video_topic := DailyVideoTopic.objects.filter(pk=pk)).exists():
                video_topic = video_topic.latest("date_added")
                next_topic_id = video_topic.next_topic_id

                if not StudentDailyVideoTopic.objects.filter(daily_video_topic=video_topic, student_profile=student_profile).exists():
                    student_daily_video_topic = StudentDailyVideoTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyVideoTopic),
                        daily_video_topic = video_topic,
                        student_profile = student_profile,
                        is_completed = True
                    )

                    if student_daily_video_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }

                elif (student_daily_video_topic := StudentDailyVideoTopic.objects.filter(daily_video_topic=video_topic, student_profile=student_profile, is_completed=False)).exists():
                    student_daily_video_topic = student_daily_video_topic.latest("date_added")
                    student_daily_video_topic.is_completed = True
                    student_daily_video_topic.save()
                    
                    if student_daily_video_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }
                
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student daily video topic already exists"
                        }
                    }
      
            elif (image_topic := DailyImageTopic.objects.filter(pk=pk)).exists():
                image_topic = image_topic.latest("date_added")
                next_topic_id = image_topic.next_topic_id

                if not StudentDailyImageTopic.objects.filter(daily_image_topic=image_topic, student_profile=student_profile).exists():
                    student_daily_image_topic = StudentDailyImageTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyImageTopic),
                        student_profile = student_profile,
                        daily_image_topic = image_topic,
                        is_completed = True
                    )

                    if student_daily_image_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }

                elif (student_daily_image_topic := StudentDailyImageTopic.objects.filter(daily_image_topic=image_topic, student_profile=student_profile)).exists():
                    student_daily_image_topic = student_daily_image_topic.latest("date_added")
                    student_daily_image_topic.is_completed = True
                    student_daily_image_topic.save()

                    if student_daily_image_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student daily video topic already exists"
                        }
                    }

            elif (text_topic := DailyTextTopic.objects.filter(pk=pk)).exists():
                text_topic = text_topic.latest("date_added")
                next_topic_id = text_topic.next_topic_id
                

                if not StudentDailyTextTopic.objects.filter(daily_text_topic=text_topic, student_profile=student_profile).exists():
                    student_daily_text_topic = StudentDailyTextTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyTextTopic),
                        daily_text_topic = text_topic,
                        student_profile = student_profile,
                        is_completed = True
                    )

                    if student_daily_text_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        } 
                   

                elif (student_daily_text_topic := StudentDailyTextTopic.objects.filter(daily_text_topic=text_topic, student_profile=student_profile, is_deleted=False)).exists():
                    student_daily_text_topic = student_daily_text_topic.latest("date_added")
                    student_daily_text_topic.is_completed = True
                    student_daily_text_topic.save()
                    
                    if student_daily_text_topic.is_completed == True:
                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily audio completed successfully"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Current topic is not completed"
                            }
                        } 
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student daily video topic already exists"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Daily topic not Found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "User not found"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['Student'])
def mark_as_complete(request, pk):
    try:
        transaction.set_autocommit(False)
        user = request.user
        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")

            if (student := StudentProfile.objects.filter(user=user, is_deleted=False)).exists():
                student = student.latest("date_added")
                programme = student.programmes

                if StudentDailyAudioTopic.objects.filter(daily_audio_topic__day=day, student_profile=student, is_completed=True, is_processed=True).exists():
                    if StudentDailyVideoTopic.objects.filter(daily_video_topic__day=day, student_profile=student, is_completed=True, is_processed=True).exists():
                        if StudentDailyTextTopic.objects.filter(daily_text_topic__day=day, student_profile=student, is_completed=True, is_processed=True).exists():
                            if StudentDailyImageTopic.objects.filter(daily_image_topic__day=day, student_profile=student, is_completed=True, is_processed=True).exists():

                                if (student_day := StudentDay.objects.filter(day=day, student__user=user, is_deleted=False)).exists():
                                    student_day = student_day.latest("date_added")

                                    student_day.status = 'completed'
                                    student_day.is_completed = True
                                    student_day.save()

                                    next_day_number = int(day.day_number) + 1
                                    if (next_day := Day.objects.filter(programme=programme, day_number=next_day_number)).exists():
                                        next_day = next_day.latest("id")

                                        if not StudentDay.objects.filter(day=next_day, student=student).exists():
                                            student_day = StudentDay.objects.create(
                                                auto_id = get_auto_id(StudentDay),
                                                day=next_day,
                                                student=student,
                                                status = 'ongoing',
                                            )

                                            transaction.commit()
                                            response_data = {
                                                "StatusCode" : 6000,
                                                "data" : {
                                                    "title" : "Success",
                                                    "message" : f"Successfully completed day-{day.day_number} and unlocked day-{next_day_number}"
                                                }
                                            }
                                        else:
                                            response_data = {
                                                "StatusCode" : 6001,
                                                "data" : {
                                                    "title" : "Failed",
                                                    "message" : "Student day already exists"
                                                }
                                            }

                                    else:
                                        response_data = {
                                            "StatusCode" : 6001,
                                            "data" : {
                                                "title" : "Failed",
                                                "message" : "An error occurred in assign next day"
                                            }
                                        }

                                    

                                else:
                                    response_data = {
                                        "StatusCode" : 6001,
                                        "data" : {
                                            "title" : "Failed",
                                            "message" : "Student day not found"
                                        }
                                    }
                            else:
                                response_data = {
                                    "StatusCode" : 6001,
                                    "data" : {
                                    "title" : "Failed",
                                    "message" : "Student daily image topic not found"
                                }
                            }
                        else:
                            response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Student daily text topic not found"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Student daily video topic not found"
                            }
                        }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student daily audio topic not found"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Student not found"
                    }
                }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Day not found"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@group_required(['EnglishCafe'])
def add_daily_topics(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddDailyTopicSerializer(data=request.data)
        if serialized_data.is_valid():
            day = request.data["day"]
            topic_type = request.data["topic_type"]
            file = request.data.get("file")
            order_id = request.data["order_id"]
            text = request.data.get("text")

            if (day := Day.objects.filter(pk=day, is_deleted=False)).exists():
                day = day.latest("id")

                if topic_type == 'audio':
                    daily_audio_topic = DailyAudioTopic.objects.create(
                        auto_id = get_auto_id(DailyAudioTopic),
                        day = day,
                        audio = file,
                        text = text,
                        order_id = order_id,
                    )

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Daily audio topic updated"
                        }
                    }
                elif topic_type == 'video':
                    daily_video_topic = DailyVideoTopic.objects.create(
                        auto_id = get_auto_id(DailyVideoTopic),
                        day = day,
                        video = file,
                        order_id = order_id,
                    )

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Daily video topic updated"
                        }
                    }
                elif topic_type == 'text':
                    daily_text_topic = DailyTextTopic.objects.create(
                        auto_id = get_auto_id(DailyTextTopic),
                        day = day,
                        daily_text = text,
                        order_id = order_id
                    )

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Daily audio text updated"
                        }
                    }
                elif topic_type == 'image':
                    daily_image_topic = DailyImageTopic.objects.create(
                        auto_id = get_auto_id(DailyImageTopic),
                        day = day,
                        daily_image = file,
                        order_id = order_id,
                    )

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Daily image topic updated"
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Topic type not found"
                        }
                    }

            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Day not found"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)



    
