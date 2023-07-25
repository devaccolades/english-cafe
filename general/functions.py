from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password

from accounts.models import ChiefProfile, StudentProfile
from courses.models import (Programme, Day, StudentDay, DailyAudioTopic, StudentDailyAudioTopic, 
                            DailyVideoTopic, StudentDailyVideoTopic, DailyImageTopic, StudentDailyImageTopic, 
                            DailyTextTopic, StudentDailyTextTopic)
from general.encryptions import encrypt


def get_auto_id(model):
    auto_id = 1
    latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        # message += "%s : %s | " %(key,error_message)
        message += f"{key} - {error_message} | "
    return message[:-3]


def loginUser(request, user):
    try:
        login(request,user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        access = {
            "access": access_token,
            "refresh": str(refresh)
        }
        return access
    except:
        error = {
            "message": "User could not be verified"
        }


# def add_day(days,)

# def add_entry_day(days):
#     obj_name = Programme.objects.get(name='Entry')
#     for i in range(days):
#         Day.objects.create(
#             programme = obj_name,
#             day_number = i + 1
#         )

# def add_advance_day(days):
#     obj_name = Programme.objects.get(name='Advanced')
#     for i in range(days):
#         Day.objects.create(
#             programme = obj_name,
#             day_number = i + 1
#         )

# def add_ielts_day(days):
#     obj_name = Programme.objects.get(name='IELTS')
#     for i in range(days):
#         Day.objects.create(
#             programme = obj_name,
#             day_number = i + 1
#         )


def CreateChiefUser(username,password):
    if not ChiefProfile.objects.filter(username=username):
        user = User.objects.create(
            username = username,
            password = make_password(password),
        )
        group_name = 'EnglishCafe'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        chief_profile = ChiefProfile.objects.create(
            auto_id = get_auto_id(ChiefProfile),
            username = username,
            password = encrypt(password),
            user = user
        )
        return "user created"
    else:
        return "user already exists"
    

def get_first_letters(string):
    words = string.split()
    
    if len(words) == 1:
        code = words[0][0].upper() + words[0][-1].upper()
    else:
        code = "".join(word[0] for word in string.split()).upper()
    
    return code


def create_student_day_for_new_student(student_data, programme):
    student_id = student_data["student_id"]
    user_pk = student_data["user_pk"]

    if Day.objects.filter(programme=programme, is_deleted=False).exists():

        day = Day.objects.filter(programme=programme, is_deleted=False).order_by('day_number').first()
        number_of_contents = day.no_of_contents

        if (student_profile := StudentProfile.objects.filter(pk=student_id,is_deleted=False)).exists():
            student_profile = student_profile.latest("date_added")

            if not StudentDay.objects.filter(day=day, student_id=student_id, is_deleted=False).exists():
                student_day = StudentDay.objects.create(
                    auto_id = get_auto_id(StudentDay),
                    day = day,
                    student = student_profile,
                    status = 'ongoing'
                )
            
        else:
            pass

    return True


def create_student_first_topic_for_a_new_student(student_data, programme):
    student_id = student_data["student_id"]
    user_pk = student_data["user_pk"]

    if Day.objects.filter(programme=programme, is_deleted=False).exists():

        day = Day.objects.filter(programme=programme, is_deleted=False).order_by('day_number').first()
        number_of_contents = day.no_of_contents

        if (student_profile := StudentProfile.objects.filter(pk=student_id,is_deleted=False)).exists():
            student_profile = student_profile.latest("date_added")

            if (daily_audio_topics := DailyAudioTopic.objects.filter(day=day, order_id=1)).exists():
                daily_audio_topics = daily_audio_topics.latest("date_added")
                if not StudentDailyAudioTopic.objects.filter(daily_audio_topic=daily_audio_topics, student_profile=student_profile).exists():
                    student_daily_topic = StudentDailyAudioTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyAudioTopic),
                        daily_audio_topic = daily_audio_topics,
                        student_profile = student_profile,
                        is_completed = False
                    )
                else:
                    print("Already Exists")

            elif (daily_video_topic := DailyVideoTopic.objects.filter(day=day, order_id=1)).exists():
                daily_video_topic = daily_video_topic.latest('date_added')
                if not StudentDailyVideoTopic.objects.filter(daily_video_topic=daily_video_topic, student_profile=student_profile).exists():
                    student_video_topic = StudentDailyVideoTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyVideoTopic),
                        daily_video_topic = daily_video_topic,
                        student_profile = student_profile,
                        is_completed = False
                    )
                else:
                    print("Already Exists")

            elif (daily_image_topic := DailyImageTopic.objects.filter(day=day, order_id=1)).exists():
                daily_image_topic = daily_image_topic.latest("date_added")
                if not StudentDailyImageTopic.objects.filter(daily_image_topic=daily_image_topic, student_profile=student_profile).exists():
                    student_image_topic = StudentDailyImageTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyImageTopic),
                        daily_image_topic = daily_image_topic,
                        student_profile = student_profile,
                        is_completed = False
                    )
                else:
                    print("Already Exists")

            elif (daily_text_topic := DailyTextTopic.objects.filter(day=day, order_id=1)).exists():
                daily_text_topic = daily_text_topic.latest("date_added")

                if not StudentDailyTextTopic.objects.filter(daily_text_topic=daily_text_topic, student_profile=student_profile).exists():
                    student_text_topic = StudentDailyTextTopic.objects.create(
                        auto_id = get_auto_id(StudentDailyTextTopic),
                        daily_text_topic = daily_text_topic,
                        student_profile = student_profile,
                        is_completed = False
                    )
                else:
                    print("Already Exists")
            
            else:
                pass
        else:
            print("Student not exists")

    return True
            


