from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password

from accounts.models import ChiefProfile
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


