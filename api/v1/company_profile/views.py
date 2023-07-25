import traceback

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from general.decorators import group_required
from general.functions import generate_serializer_errors, get_auto_id
from api.v1.company_profile.serializers import *
from company_profile.models import *


@api_view(['POST'])
@group_required(['EnglishCafe'])
def add_achievement(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddAchievementsSerializer(data=request.data)
        if serialized_data.is_valid():
            title = request.data["title"]
            description = request.data["description"]
            image = request.data.get("image")

            if not Achievements.objects.filter(title=title,description=description).exists():
                achievements = Achievements.objects.create(
                    auto_id = get_auto_id(Achievements),
                    title = title,
                    description = description,
                    image =image
                )

                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Achievements added successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Same achievement already exists"
                    }
                }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" :generate_serializer_errors(serialized_data._errors)
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
@group_required(['EnglishCafe', 'Student',])
def achievements_view(request):
    try:
        transaction.set_autocommit(False)
        if (achievements := Achievements.objects.filter(is_deleted=False)).exists():

            serialized_data = AchievementListSerializer(
                achievements,
                context = {
                    "request" : request
                },
                many=True,
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
                    "message" : "Achievements not found"
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except  Exception as e:
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
def edit_achievements(request,pk):
    try:
        transaction.set_autocommit(False)
        title = request.data.get("title")
        image = request.data.get("image")
        description = request.data.get("description")

        if (achievements := Achievements.objects.filter(pk=pk, is_deleted=False)).exists():
            achievement = achievements.latest("date_added")

            if title:
                achievement.title = title
            if image:
                achievement.image = image
            if description:
                achievement.description = description

            achievement.save()

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
                "data" : {
                    "title" : "Failed",
                    "message" : "Achievements not found"
                }
            }
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except  Exception as e:
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
def single_achievements(request,pk):
    try:
        transaction.set_autocommit(False)
        if (achievements := Achievements.objects.filter(pk=pk, is_deleted=False)).exists():
            achievement = achievements.latest("date_added")

            serialized_data = AchievementListSerializer(
                achievement,
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
                    "message" : "Achievements not found"
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
    except  Exception as e:
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
def add_testimonials(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddTestimonialSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            quote = request.data["quote"]
            image = request.data["image"]
            rating_count = request.data["rating_count"]
            video = request.data.get("video")

            if not Testimonials.objects.filter(name=name, quote=quote, image=image, rating_count=rating_count).exists():

                testimonials = Testimonials.objects.create(
                    auto_id = get_auto_id(Testimonials),
                    name = name,
                    quote = quote,
                    image = image,
                    rating_count = rating_count,
                    video = video
                )

                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Testimonial added successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Testimonial already exists"
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

    except  Exception as e:
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
@permission_classes([AllowAny])
def view_testimonials(request):
    try:
        transaction.set_autocommit(False)
        if (testimonials := Testimonials.objects.filter(is_deleted=False)).exists():

            serialized_data = TestimonialListSerializer(
                testimonials,
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
                    "message" : "Testimonials not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def edit_testimonials(request, pk):
    try:
        transaction.set_autocommit(False)
        name = request.data.get("name")
        quote = request.data.get("quote")
        rating_count = request.data.get("rating_count")
        image = request.data.get("image")
        video = request.data.get("video")

        if (testimonial := Testimonials.objects.filter(pk=pk, is_deleted=False)).exists():
            testimonial = testimonial.latest("date_added")

            if name:
                testimonial.name = name
            if quote:
                testimonial.quote = quote
            if rating_count:
                testimonial.rating_count = rating_count
            if image:
                testimonial.image = image
            if video:
                testimonial.video = video

            testimonial.save()

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
                "data" : {
                    "title" : "Failed",
                    "message" : "Testimonial not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def single_testimonials(request, pk):
    try:
        transaction.set_autocommit(False)
        if (testimonial := Testimonials.objects.filter(pk=pk, is_deleted=False)).exists():
            testimonial = testimonial.latest("date_added")

            serialized_data = TestimonialListSerializer(
                testimonial,
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
                    "message" : "Testimonial not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def delete_testimonials(request, pk):
    try:
        transaction.set_autocommit(False)
        if (testimonial := Testimonials.objects.filter(pk=pk, is_deleted=False)).exists():
            testimonial = testimonial.latest("date_added")

            testimonial.is_deleted = True
            testimonial.save()

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "testimonial deleted successfully"
                }
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Testimonial not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)
        
    except  Exception as e:
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
def add_our_team(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddOurTeamSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            photo = request.data["photo"]
            designation = request.data["designation"]

            our_team = OurTeam.objects.create(
                auto_id = get_auto_id(OurTeam),
                name = name,
                photo = photo,
                designation = designation,
            )

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Our team added successfully"
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
    except  Exception as e:
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
@permission_classes([AllowAny,])
def get_our_team(request):
    try:
        transaction.set_autocommit(False)
        if (our_teams := OurTeam.objects.filter(is_deleted=False)).exists():

            serialized_data = OurTeamListSerializer(
                our_teams,
                context = {
                    "request" : request
                },
                many=True
            ).data

            response_data = {
                'StatusCode' : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Our team not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def delete_our_team(request, pk):
    try:
        transaction.set_autocommit(False)

        if (our_team := OurTeam.objects.filter(is_deleted=False)).exists():
            our_team = our_team.latest("date_added")

            our_team.is_deleted =True
            our_team.save()

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Team member deleted successfully"
                }
            }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Our team not found"
                }
            }
        
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def add_careers(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddCareerSerializer(data=request.data)
        if serialized_data.is_valid():
            designation = request.data["designation"]
            job_description = request.data["job_description"]
            job_type = request.data["job_type"]

            careers = Career.objects.create(
                auto_id = get_auto_id(Career),
                designation = designation,
                job_description = job_description,
                job_type = job_type,
            )

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Career added successfully"
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

    except  Exception as e:
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
@group_required(['EnglishCafe', 'Student'])
def view_careers(request):
    try:
        transaction.set_autocommit(False)
        if (careers := Career.objects.filter(is_deleted=False)).exists():

            serialized_data = CareerListSerializer(
                careers,
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
                    "message" : "Career not found"
                }
            }

        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def delete_careers(request, pk):
    try:
        transaction.set_autocommit(False)
        if (career :=  Career.objects.filter(pk=pk, is_deleted=False)).exists():
            career = career.latest("date_added")

            career.is_deleted = False
            career.save()

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Career deleted successfully"
                }
            }

        else:
            response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "title" : "Failed",
                    "message" : "Career not found"
                }
            }
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except  Exception as e:
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
def create_career_enquiry(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddCareerEnquirySerializer(data=request.data)
        if serialized_data.is_valid():
            job = request.data["job"]
            name = request.data["name"]
            phone = request.data["phone"]
            email = request.data["email"]
            cv = request.data["cv"]

            if (career := Career.objects.filter(pk=job, is_deleted=False)).exists():
                career = career.latest("date_added")

                career_enquiry = CareerEnquiry.objects.create(
                    auto_id = get_auto_id(CareerEnquiry),
                    job = career,
                    name = name,
                    phone = phone,
                    email = email,
                    cv = cv
                )

                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Created career enquiry successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Career not found"
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

    except  Exception as e:
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
    



    

    









    
