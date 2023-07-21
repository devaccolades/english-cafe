from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from general.decorators import group_required
from courses.models import *
from api.v1.courses.serializers import *



@api_view(['GET'])
@group_required(['Student'])
def get_daily_topics(request, pk):
    try:
        if (day := Day.objects.filter(pk=pk, is_deleted=False)).exists():
            day = day.latest("id")

            number = day.no_of_contents

            topics =[]

            for i in range(int(day.no_of_contents)):

                if (daily_audio_topics := DailyAudioTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                    audio_serialized_data = DailyAudioTopicSerializer(
                        daily_audio_topics,
                        context = {
                            "request" : request,
                        },
                        many=True
                    ).data
                    audio_serialized_data[0]['type'] = "audio"
                    topics.append(audio_serialized_data[0])
                else:
                    pass

                if (daily_video_topics := DailyVideoTopic.objects.filter(day=day, order_id=int(i+1))).exists():
                    video_serialized_data = DailyVideoTopicSerializer(
                        daily_video_topics,
                        context = {
                            "request" : request,
                        },
                        many=True
                    ).data

                    video_serialized_data[0]["type"] = "video"
                    topics.append(video_serialized_data[0])
                else:
                    pass

                if (daily_image_topic := DailyImageTopic.objects.filter(day=day, order_id=int(i+1))).exists():

                    image_serialized_data = DailyImageTopicSerializer(
                        daily_image_topic,
                        context = {
                            "request" : request
                        },
                        many=True
                    ).data

                    image_serialized_data[0]["type"] = "image"
                    topics.append(image_serialized_data[0])
                else:
                    pass


                if (daily_text_topic := DailyTextTopic.objects.filter(day=day, order_id=int(i+1))).exists():

                    text_serialized_data = DailyTextSerializer(
                        daily_text_topic,
                        context = {
                            "request" : request
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
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except Exception as E:
        return Response({'app_data': 'something went wrong', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)