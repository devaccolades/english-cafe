import traceback

from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from general.decorators import group_required
from general.functions import generate_serializer_errors, get_auto_id, assing_first_topic_of_a_day
from courses.models import *
from accounts.models import StudentProfile
from api.v1.courses.serializers import *
from api.v1.courses.functions import assign_next_topic, convert_to_mp3


@api_view(['GET'])
@permission_classes([AllowAny,])
def programme_list(request):
    try:
        transaction.set_autocommit(False)
        if (programmes := Programme.objects.filter(is_deleted=False)).exists():
            programmes = programmes.order_by('order_id')
            
            serialized_data = ProgrammeListSerializers(
                programmes,
                context = {
                    "request" : request
                },
                many=True
            ).data

            transaction.commit()
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
@group_required(['Student','EnglishCafe'])
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

                    if (daily_audio_topics := DailyAudioTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
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

                    if (daily_video_topics := DailyVideoTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
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

                    if (daily_image_topic := DailyImageTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
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


                    if (daily_text_topic := DailyTextTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
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
    

@api_view(['GET'])
@group_required(['EnglishCafe'])
def get_admin_daily_topics(request, pk):
    try:
        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")
            if day.no_of_contents:
                number_of_contents_in_a_day = day.no_of_contents
            else:
                number_of_contents_in_a_day = 0

            topics =[]
            temp_data = []

            for i in range(int(number_of_contents_in_a_day)):

                if (daily_audio_topics := DailyAudioTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
                    daily_audio_topic_object = daily_audio_topics.latest("date_added")
                    if not temp_data:
                        temp_data.append(daily_audio_topic_object)
                    else:
                        temp_data[-1].next_topic_id = daily_audio_topic_object.id
                        temp_data[-1].save()
                        temp_data.append(daily_audio_topic_object)

                    audio_serialized_data = DailyAdminAudioTopicSerializer(
                        daily_audio_topics,
                        context = {
                            "request" : request,
                            # "student_id" : student,
                        },
                        many=True
                    ).data
                    audio_serialized_data[0]['type'] = "audio"
                    topics.append(audio_serialized_data[0])
                else:
                    pass

                if (daily_video_topics := DailyVideoTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
                    daily_video_topics_object = daily_video_topics.latest("date_added")

                    if not temp_data:
                        temp_data.append(daily_video_topics_object)
                    else:
                        temp_data[-1].next_topic_id = daily_video_topics_object.id
                        temp_data[-1].save()
                        temp_data.append(daily_video_topics_object)

                    video_serialized_data = DailyAdminVideoTopicSerializer(
                        daily_video_topics,
                        context = {
                            "request" : request,
                            # "student_id" : student,
                        },
                        many=True
                    ).data

                    video_serialized_data[0]["type"] = "video"
                    topics.append(video_serialized_data[0])
                else:
                    pass

                if (daily_image_topic := DailyImageTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
                    daily_image_topic_objects = daily_image_topic.latest("date_added")

                    if not temp_data:
                        temp_data.append(daily_image_topic_objects)
                    else:
                        temp_data[-1].next_topic_id = daily_image_topic_objects.id
                        temp_data[-1].save()
                        temp_data.append(daily_image_topic_objects)

                    image_serialized_data = DailyAdminImageTopicSerializer(
                        daily_image_topic,
                        context = {
                            "request" : request,
                            # "student_id" : student,
                        },
                        many=True
                    ).data

                    image_serialized_data[0]["type"] = "image"
                    topics.append(image_serialized_data[0])
                else:
                    pass


                if (daily_text_topic := DailyTextTopic.objects.filter(day=day, order_id=int(i+1), is_deleted=False)).exists():
                    daily_text_topic_object = daily_text_topic.latest("date_added")

                    if not temp_data:
                        temp_data.append(daily_text_topic_object)
                    else:
                        temp_data[-1].next_topic_id = daily_text_topic_object.id
                        temp_data[-1].save()
                        temp_data.append(daily_text_topic_object)

                    text_serialized_data = DailyAdminTextSerializer(
                        daily_text_topic,
                        context = {
                            "request" : request,
                            # "student_id" : student,
                        },
                        many=True
                    ).data

                    text_serialized_data[0]["type"] = "text"
                    topics.append(text_serialized_data[0])

            response_data = {
                "StatusCode" : 6000,
                "number_of_contents_in_a_day":number_of_contents_in_a_day,
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
def daily_topic_complete(request, pk):
    try:
        transaction.set_autocommit(False)
        user = request.user

        if (student_profile := StudentProfile.objects.filter(user=user)).exists():
            student_profile = student_profile.latest("date_added")

            if (audio_topic := DailyAudioTopic.objects.filter(pk=pk, is_deleted=False)).exists():
                audio_topic = audio_topic.latest("date_added")
                next_topic_id = audio_topic.next_topic_id

                if not StudentDailyAudioTopic.objects.filter(daily_audio_topic=audio_topic, student_profile=student_profile, is_processed=True, is_deleted=False).exists():
                    student_audio_topic = StudentDailyAudioTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyAudioTopic),
                        daily_audio_topic = audio_topic,
                        student_profile = student_profile,
                        is_processed = True,
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
                elif (student_daily_audio_topic := StudentDailyAudioTopic.objects.filter(daily_audio_topic=audio_topic, student_profile=student_profile, is_processed=True,is_completed=False, is_deleted=False)).exists():
                    print("come to elif function")
                    student_daily_audio_topic = student_daily_audio_topic.latest("date_added")
                    student_daily_audio_topic.is_completed = True
                    student_daily_audio_topic.save()
                    
                    if student_daily_audio_topic.is_completed == True:

                        if next_topic_id == None:
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Milestone Reached!"
                                }
                            }
                            return Response({'app_data': response_data}, status=status.HTTP_200_OK)
                        else:
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
                            "message" : f"Student {audio_topic.day} audio topic not found or it has not been processed yet"
                        }
                    }

            elif (video_topic := DailyVideoTopic.objects.filter(pk=pk, is_deleted=False)).exists():
                video_topic = video_topic.latest("date_added")
                next_topic_id = video_topic.next_topic_id

                if not StudentDailyVideoTopic.objects.filter(daily_video_topic=video_topic, student_profile=student_profile, is_processed=True, is_deleted=False).exists():
                    student_daily_video_topic = StudentDailyVideoTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyVideoTopic),
                        daily_video_topic = video_topic,
                        student_profile = student_profile,
                        is_processed = True,
                        is_completed = True
                    )

                    if student_daily_video_topic.is_completed == True:

                        assign_next_topic(next_topic_id, student_profile)
                
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily video completed successfully"
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

                elif (student_daily_video_topic := StudentDailyVideoTopic.objects.filter(daily_video_topic=video_topic, student_profile=student_profile, is_processed=True, is_completed=False, is_deleted=False)).exists():
                    student_daily_video_topic = student_daily_video_topic.latest("date_added")
                    student_daily_video_topic.is_completed = True
                    student_daily_video_topic.save()
                    
                    if student_daily_video_topic.is_completed == True:

                        if next_topic_id == None:
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Milestone Reached!"
                                }
                            }
                            return Response({'app_data': response_data}, status=status.HTTP_200_OK)
                        else:
                            assign_next_topic(next_topic_id, student_profile)
                
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily video completed successfully"
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
                            "message" : f"Student {video_topic.day} video topic not found or it has not been processed yet"
                        }
                    }
      
            elif (image_topic := DailyImageTopic.objects.filter(pk=pk, is_deleted=False)).exists():
                image_topic = image_topic.latest("date_added")
                next_topic_id = image_topic.next_topic_id

                if not StudentDailyImageTopic.objects.filter(daily_image_topic=image_topic, student_profile=student_profile, is_processed=True, is_deleted=False).exists():
                        student_daily_image_topic = StudentDailyImageTopic.objects.create(
                            auto_id = get_auto_id(StudentDailyImageTopic),
                            student_profile = student_profile,
                            daily_image_topic = image_topic,
                            is_processed = True,
                            is_completed = True
                        )

                        if student_daily_image_topic.is_completed == True:

                            assign_next_topic(next_topic_id, student_profile)
                    
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Student daily image completed successfully"
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
                    

                elif (student_daily_image_topic := StudentDailyImageTopic.objects.filter(daily_image_topic=image_topic, student_profile=student_profile, is_processed=True, is_deleted=False)).exists():
                    student_daily_image_topic = student_daily_image_topic.latest("date_added")
                    student_daily_image_topic.is_completed = True
                    student_daily_image_topic.save()

                    if student_daily_image_topic.is_completed == True:

                        if next_topic_id == None:
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Milestone Reached!"
                                }
                            }
                            return Response({'app_data': response_data}, status=status.HTTP_200_OK)
                        else:
                            assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily image completed successfully"
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
                            "message" : f"Student {image_topic.day} image topic not found or it has not been processed yet"
                        }
                    }

            elif (text_topic := DailyTextTopic.objects.filter(pk=pk, is_deleted=False)).exists():
                text_topic = text_topic.latest("date_added")
                next_topic_id = text_topic.next_topic_id
                
                if not StudentDailyTextTopic.objects.filter(daily_text_topic=text_topic, student_profile=student_profile, is_processed=True, is_deleted=False).exists():
                    student_daily_text_topic = StudentDailyTextTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyTextTopic),
                        daily_text_topic = text_topic,
                        student_profile = student_profile,
                        is_processed = True,
                        is_completed = True
                    )

                    if student_daily_text_topic.is_completed == True:


                        assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily text completed successfully"
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
                   

                elif (student_daily_text_topic := StudentDailyTextTopic.objects.filter(daily_text_topic=text_topic, student_profile=student_profile, is_processed=True,is_completed=False, is_deleted=False)).exists():
                    student_daily_text_topic = student_daily_text_topic.latest("date_added")

                    student_daily_text_topic.is_completed = True
                    student_daily_text_topic.save()
                    
                    if student_daily_text_topic.is_completed:

                        if next_topic_id == None:
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Milestone Reached!"
                                }
                            }
                            return Response({'app_data': response_data}, status=status.HTTP_200_OK)
                        else:
                            assign_next_topic(next_topic_id, student_profile)
                    
                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Student daily text completed successfully"
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
                            "message" :  f"Student {text_topic.day} text topic not found or it has not been processed yet"
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
            day_number = day.day_number
            next_day_number = day_number + 1

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

                                            student_data = {
                                                "student_id" : student.id,
                                                "user_pk" : student.user.id
                                            }

                                            # if (next_day := Day.objects.filter(programme=programme, day_number=next_day_number)).exists():
                                            #     next_day = next_day.latest("id")

                                            assing_first_topic_of_a_day(student_data, programme, next_day_number)

                                            transaction.commit()
                                            response_data = {
                                                "StatusCode" : 6000,
                                                "data" : {
                                                    "title" : "Success",
                                                    "message" : "Successfully completed the current day",
                                                    "next_day_id" : next_day.id
                                                }
                                            }
                                            # else:
                                            #     if (last_day := Day.objects.filter(programme=programme, is_deleted=False)).exists():
                                            #         last_day = last_day.latest("day_number")

                                            #         if next_day_number == last_day.day_number:
                                                        
                                            #             if (last_student_day := StudentDay.objects.filter(day=last_day, student=student, is_complete=True, status='completed')).exists():

                                            #                 response_data = {
                                            #                     "StatusCode" : 6000,
                                            #                     "data" : {
                                            #                         "title" : "Success",
                                            #                         "message" : f"{programme} completed successfully"
                                            #                     }
                                            #                 }
                                            #             else:
                                            #                 pass
                                            #         else:
                                            #             pass
                                            #     else:
                                            #         response_data = {
                                            #             "StatusCode" : 6001,
                                            #             "data" : {
                                            #                 "title" : "Failed",
                                            #                 "message" : "An error occured"
                                            #             }
                                            #         }

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
                                            "StatusCode" : 6000,
                                            "data" : {
                                                "title" : "Success",
                                                "message" : f"{programme} completed successfully"
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
                                    "message" : "Student daily image topic not complete"
                                }
                            }
                        else:
                            response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Student daily text topic not complete"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Student daily video topic not complete"
                            }
                        }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student daily audio topic not complete"
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


@api_view(['GET'])
@group_required(['Student'])
def current_day(request):
    try:
        user = request.user
        if (student := StudentProfile.objects.filter(user=user, is_deleted=False)).exists():
            student = student.latest("date_added")

            if (student_day := StudentDay.objects.filter(student=student, is_completed=False, status='ongoing')).exists():
                student_day = student_day.latest("date_added")
                current_day_id = student_day.day.id

                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "current_day_id" : current_day_id
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
                    "message" : "Student not found"
                }
            }
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
def add_programme(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddProgrammeSerializer(data = request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            duration = request.data["duration"]
            description = request.data["description"]
            order_id = request.data["order_id"]

            if not Programme.objects.filter(order_id=order_id, is_deleted=False).exists():

                programme = Programme.objects.create(
                    auto_id = get_auto_id(Programme),
                    name = name,
                    duration = duration,
                    description = description,
                    order_id = order_id
                )
                
                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : f'{programme.name} programme created successfully'
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Order id  already exists"
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


@api_view(['POST'])
@group_required(['EnglishCafe'])
def edit_programme(request, pk):
    try:
        transaction.set_autocommit(False)
        programme_name = request.data.get("programme_name")
        duration = request.data.get("duration")
        description  = request.data.get("description")
        order_id = request.data.get("order_id")

        if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
            programme = programme.latest("date_added")

            if programme_name:
                programme.name = programme_name
            if duration:
                programme.duration = duration
            if description:
                programme.description = description
            if order_id:
                programme.order_id = order_id

            programme.save()
            transaction.commit()

            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Edit completed successfully"
                }
            }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" :{
                    "title" : "Failed",
                    "message" : "Programme not found"
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
@group_required(['EnglishCafe'])
def programme(request, pk):
    try:
        transaction.set_autocommit(False)
        
        if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
            programme = programme.latest("date_added")

            serialized_data = ProgrammeListSerializers(
                programme,
                context = {
                    "request" : request
                },
            ).data

            transaction.commit()
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
def delete_programme(request, pk):
    try:
        transaction.set_autocommit(False)
        if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
            programme = programme.latest("date_added")
            programme.is_deleted = True
            programme.save()

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Programme deleted successfully"
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
            order_id = request.data["order_id"]
            audio_text = request.data.get("audio_text")
            text = request.data.get("text")
            try:
                file = request.FILES['file']
            except:
                file = None

            if (day := Day.objects.filter(pk=day, is_deleted=False)).exists():
                day = day.latest("id")

                if day.no_of_contents:

                    if topic_type == 'audio':
                        try:
                            to_mp3_file = convert_to_mp3(file)
                            daily_audio_topic = DailyAudioTopic.objects.create(
                                auto_id = get_auto_id(DailyAudioTopic),
                                day = day,
                                audio = to_mp3_file,
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
                        except Exception as e:
                            response_data = {
                                "StatusCode" : 6001,
                                "data" : {
                                    "title" : "Conversion or saving failed",
                                    "message" : str(e)
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
                                "message" : "Daily text topic updated"
                            }
                        }
                    elif topic_type == 'video':
                        daily_video_topic = DailyVideoTopic.objects.create(
                            auto_id = get_auto_id(DailyVideoTopic),
                            day = day,
                            video = file,
                            order_id = order_id
                        )

                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : "Daily video topic updated"
                            }
                        }
                    elif topic_type == 'image':
                        daily_image_topic = DailyImageTopic.objects.create(
                            auto_id = get_auto_id(DailyImageTopic),
                            day = day,
                            daily_image = file,
                            order_id = order_id
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
                            "message" : "No of content not found"
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


@api_view(['GET'])
@group_required(['EnglishCafe'])
def single_topic(request, pk):
    try:
        if (daily_audio_topics := DailyAudioTopic.objects.filter(pk=pk,  is_deleted=False)).exists():
            daily_audio_topics = daily_audio_topics.latest("date_added")
            
            serialized_data = DailyAdminAudioTopicSerializer(
                daily_audio_topics,
                context = {
                    "request" : request,
                },
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }


        elif (daily_video_topics := DailyVideoTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_video_topics = daily_video_topics.latest("date_added")

            serialized_data = DailyAdminVideoTopicSerializer(
                daily_video_topics,
                context = {
                    "request" : request,
                },
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }


        elif (daily_image_topic := DailyImageTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_image_topic = daily_image_topic.latest("date_added")

            serialized_data = DailyAdminImageTopicSerializer(
                daily_image_topic,
                context = {
                    "request" : request,
                },
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }

        elif (daily_text_topic := DailyTextTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_text_topic = daily_text_topic.latest("date_added")

            serialized_data = DailyAdminTextSerializer(
                daily_text_topic,
                context = {
                    "request" : request,
                },
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
                    "message" : "Daily topic not found"
                }
            }
            
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
def edit_daily_topics(request, pk):
    try:
        transaction.set_autocommit(False)

        file = request.data.get("file")
        text = request.data.get("text")
        order_id = request.data.get("order_id")
        
        if (daily_topics := DailyAudioTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")

            if file:
                daily_topics.audio = file
            if order_id:
                daily_topics.order_id = order_id
            
            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily audio topic edited successfully"
            }
        elif (daily_topics := DailyTextTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")

            if order_id:
                daily_topics.order_id = order_id
            if text:
                daily_topics.daily_text = text

            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily text topic edited successfully"
            }
        elif (daily_topics := DailyImageTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")

            if file:
                daily_topics.daily_image = file
            if order_id:
                daily_topics.order_id = order_id

            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily video image edited successfully"
            }
        elif (daily_topics := DailyVideoTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")

            if file:
                daily_topics.video = file
            if order_id:
                daily_topics.order_id = order_id

            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily video topic edited successfully"
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "title" : "Failed",
                "message" : "Daily topic not found"
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
def delete_daily_topics(request, pk):
    try:
        
        if (daily_topics := DailyAudioTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")
            daily_topics.is_deleted = True
            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily audio topic deleted successfully"
            }
        elif (daily_topics := DailyTextTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")
            daily_topics.is_deleted = True
            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily text topic deleted successfully"
            }
        elif (daily_topics := DailyImageTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")
            daily_topics.is_deleted = True
            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily video image deleted successfully"
            }
        elif (daily_topics := DailyVideoTopic.objects.filter(pk=pk, is_deleted=False)).exists():
            daily_topics = daily_topics.latest("date_added")
            daily_topics.is_deleted = True
            daily_topics.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "title" : "Success",
                "message" : "Daily video topic deleted successfully"
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "title" : "Failed",
                "message" : "Daily topic not found"
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
@group_required(['EnglishCafe'])
def days_list_programme(request):
    try:
        transaction.set_autocommit(False)

        programme_id = request.GET.get("programme_id")

        if programme_id:

            if (programme := Programme.objects.filter(pk=programme_id,is_deleted=False)).exists():
                programme = programme.latest("date_added")

                if (days := Day.objects.filter(programme=programme, is_deleted=False)).exists():
                    days = days.order_by('day_number')
                    serialized_data = AdminDayListSerializer(
                        days,
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
                            "message" : "Day not found"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" :{
                        "title" : "Failed",
                        "message" : "Programme not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Programme id not found"
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
def add_days(request, pk):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddDaysSerializer(data = request.data)
        if serialized_data.is_valid():
            days = request.data["days"]
            days = int(days)

            if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
                programme = programme.latest("date_added")

                if not Day.objects.filter(programme=programme).exists():
                    for i in range(days):
                        Day.objects.create(
                            programme = programme,
                            day_number = i + 1
                        )
                    
                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : f'{programme.name} days added successfully'
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Days already exists in this programme"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['EnglishCafe'])
def add_day(request, pk):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddDaySerializer(data=request.data)
        if serialized_data.is_valid():
            day_number = request.data['day_number']
            no_of_content = request.data.get("no_of_content")

            if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
                programme = programme.latest("date_added")

                if (day := Day.objects.filter(programme=programme)).exists():
                    day = day.latest("day_number")

                    if not Day.objects.filter(programme=programme, day_number=day_number).exists():
                        
                        new_day = Day.objects.create(
                            programme = programme,
                            day_number = day_number,
                            no_of_contents = no_of_content
                        )

                        transaction.commit()
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : {
                                "title" : "Success",
                                "message" : f"Day {new_day.day_number} added in the {programme} programme"
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Day already exists in this programme"
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

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['EnglishCafe'])
def add_number_of_content(request, pk):
    try:
        transaction.set_autocommit(False)
        number_of_content = request.data.get("number_of_content")

        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")

            if number_of_content:
                day.no_of_contents = number_of_content

            day.save()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "number of content added successfully"
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

@api_view(['GET'])
@group_required(['EnglishCafe'])
def number_of_content(request, pk):
    try:
        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")
            if day.no_of_contents:
                number_of_content = int(day.no_of_contents)
            else:
                number_of_content = 0
            
            response_data = {
                "StatusCode" : 6000,
                "number_of_content" : number_of_content
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Day not found"             
                }
            }
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
@group_required(['EnglishCafe'])
def student_count(request):
    try:
        transaction.set_autocommit(False)
        count_data = []
        count_obj = {}
        if (programmes := Programme.objects.filter(is_deleted=False)).exists():

            for programme in programmes:
                if (student_profile := StudentProfile.objects.filter(programmes=programme)).exists():
                    student_profile_programme_count = student_profile.count()

                    count_obj = {
                        "programme" : programme.name,
                        "count" : student_profile_programme_count
                    }

                    count_data.append(count_obj)

                    response_data = {
                        "StatusCode" : 6000,
                        "programme" : count_data
                    }

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
def delete_days(request, pk):
    try:
        transaction.set_autocommit(False)
        if (programme := Programme.objects.filter(pk=pk, is_deleted=False)).exists():
            programme = programme.latest("date_added")

            if (days := Day.objects.filter(programme=programme, is_deleted=False)).exists():
                for day in days:
                    day.delete()
                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "all days deleted successfully"
                         }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Days not found"
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
def delete_single_day(request, pk):
    try:
        transaction.set_autocommit(False)
        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")
            day.delete()
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Day deleted successfully"
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


    






    
