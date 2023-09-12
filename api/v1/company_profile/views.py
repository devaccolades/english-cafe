import traceback

from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from general.decorators import group_required
from general.functions import generate_serializer_errors, get_auto_id, send_emails
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
            description = request.data.get("description")
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
@permission_classes([AllowAny,])
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
def delete_achievements(request, pk):
    try:
        transaction.set_autocommit(False)
        if (achievements := Achievements.objects.filter(pk=pk, is_deleted=False)).exists():
            achievements = achievements.latest("date_added")
            achievements.delete()

            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "achievement deleted successfully"
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
    

@api_view(['POST'])
@group_required(['EnglishCafe'])
def add_testimonials(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddTestimonialSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            quote = request.data["quote"]
            rating_count = request.data["rating_count"]
            video = request.data.get("video")
            try:
                image = request.data["image"]
            except:
                image = None

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
        q = request.GET.get("q")
        if (testimonials := Testimonials.objects.filter(is_deleted=False)).exists():

            if q:
                testimonials = Testimonials.objects.filter(name__icontains=q , is_deleted=False)

            paginator = Paginator(testimonials, 20)
            page = request.GET.get('page')
            try:
                testimonials = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                testimonials = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                testimonials = paginator.page(paginator.num_pages)

            next_page_number = 1
            has_next_page = False
            if testimonials.has_next():
                has_next_page = True
                next_page_number = testimonials.next_page_number()

            has_previous_page = False
            previous_page_number = 1
            if testimonials.has_previous():
                has_previous_page = True
                previous_page_number = testimonials.previous_page_number()

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
                "data" : serialized_data,
                'pagination_data': {
                    'current_page': testimonials.number,
                    'has_next_page': has_next_page,
                    'next_page_number': next_page_number,
                    'has_previous_page': has_previous_page,
                    'previous_page_number': previous_page_number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'first_item': testimonials.start_index(),
                    'last_item': testimonials.end_index(),
                },
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
            testimonial.delete()

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
    

@api_view(['GET'])
@group_required(['EnglishCafe'])
def get_department(request):
    try:
        transaction.set_autocommit(False)
        if (departments := Department.objects.filter(is_deleted=False)).exists():

            serialized_data = ViewDepartMentSerializer(
                departments,
                context = {
                    "request" : request,
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
                    "message" : "Deaprtment not found"
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
            head = request.data["head"]
            department = request.data["department"]

            if (pannel := Department.objects.filter(pk=department, is_deleted=False)).exists():
                pannel = pannel.latest("date_added")

                our_team = OurTeam.objects.create(
                    auto_id = get_auto_id(OurTeam),
                    name = name,
                    photo = photo,
                    designation = designation,
                    department = pannel,
                    head = head,
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
                        "message" : "Department not found"
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
        if (department := Department.objects.filter(is_deleted=False)).exists():

            serialized_data = OurTeamDepartmentSerializer(
                department,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }

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
def get_our_team_admin(request):
    try:
        transaction.set_autocommit(False)
        q = request.GET.get("q")
        if (our_teams := OurTeam.objects.filter(is_deleted=False)).exists():
            if q:
                our_teams = OurTeam.objects.filter(Q(name__icontains=q) | Q(designation__icontains=q), is_deleted=False)

            paginator = Paginator(our_teams, 20)
            page = request.GET.get('page')
            try:
                our_teams = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                our_teams = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                our_teams = paginator.page(paginator.num_pages)

            next_page_number = 1
            has_next_page = False
            if our_teams.has_next():
                has_next_page = True
                next_page_number = our_teams.next_page_number()

            has_previous_page = False
            previous_page_number = 1
            if our_teams.has_previous():
                has_previous_page = True
                previous_page_number = our_teams.previous_page_number()

            serialized_data = OurTeamListSerializer(
                our_teams,
                context = {
                    "request" : request
                },
                many=True
            ).data

            response_data = {
                'StatusCode' : 6000,
                "data" : serialized_data,
                'pagination_data': {
                    'current_page': our_teams.number,
                    'has_next_page': has_next_page,
                    'next_page_number': next_page_number,
                    'has_previous_page': has_previous_page,
                    'previous_page_number': previous_page_number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'first_item': our_teams.start_index(),
                    'last_item': our_teams.end_index(),
                },
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
    

@api_view(['GET'])
@group_required(['EnglishCafe'])
def our_team(request, pk):
    try:
        transaction.set_autocommit(False)
        if (our_team := OurTeam.objects.filter(pk=pk)).exists():
            our_team = our_team.latest("date_added")

            serialized_data = OurTeamListSerializer(
                our_team,
                context = {
                    "request" : request
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
def edit_our_team(request, pk):
    try:
        transaction.set_autocommit(False)
        name = request.data.get("name")
        photo = request.data.get("photo")
        designation = request.data.get("designation")
        head = request.data.get("head")
        department = request.data.get("department")

        if (our_team := OurTeam.objects.filter(pk=pk, is_deleted=False)).exists():
            our_team = our_team.latest("date_added")

            if name:
                our_team.name = name
            if photo:
                our_team.photo = photo
            if designation:
                our_team.designation = designation
            if head:
                our_team.head = head
            if department:
                if (instance := Department.objects.filter(pk=department, is_deleted=False)).exists():
                    instance = instance.latest("date_added")
                    our_team.department = instance

            our_team.save()
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
            our_team.delete()

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
@permission_classes([AllowAny,])
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
            career.delete()

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
@permission_classes([AllowAny,])
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

                transaction.commit()
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
    

@api_view(['GET'])
@permission_classes([AllowAny,])
def company_count_data(request):
    try:
        if (company_count := CompanyCount.objects.filter(is_deleted=False)).exists():

            serialized_data = CompanyCountListSerializer(
                company_count,
                context  = {
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
                    "message" : "Company count not found"
                }
            }
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
def get_career_enquiry(request):
    try:
        transaction.set_autocommit(False)
        q = request.GET.get("q")
        if (career_enquiries := CareerEnquiry.objects.filter(is_deleted=False)).exists():
            career_enquiries = career_enquiries.order_by("-date_added")

            if q:
                career_enquiries = CareerEnquiry.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(job__designation__icontains=q), is_deleted=False)

            paginator = Paginator(career_enquiries, 20)
            page = request.GET.get('page')
            try:
                career_enquiries = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                career_enquiries = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                career_enquiries = paginator.page(paginator.num_pages)

            next_page_number = 1
            has_next_page = False
            if career_enquiries.has_next():
                has_next_page = True
                next_page_number = career_enquiries.next_page_number()

            has_previous_page = False
            previous_page_number = 1
            if career_enquiries.has_previous():
                has_previous_page = True
                previous_page_number = career_enquiries.previous_page_number()

            serialized_data = CareerEnquirySerializer(
                career_enquiries,
                context = {
                    "request" : request
                },
                many=True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data,
                'pagination_data': {
                    'current_page': career_enquiries.number,
                    'has_next_page': has_next_page,
                    'next_page_number': next_page_number,
                    'has_previous_page': has_previous_page,
                    'previous_page_number': previous_page_number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'first_item': career_enquiries.start_index(),
                    'last_item': career_enquiries.end_index(),
                },
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Career enquiry not found"
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
def get_enquiry(request):
    try:
        q = request.GET.get("q")
        if (enquiry := Enquiry.objects.filter(is_deleted=False)).exists():

            if q:
                enquiry = Enquiry.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q),is_deleted=False)
           
            paginator = Paginator(enquiry, 20)
            page = request.GET.get('page')
            try:
                enquiry = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                enquiry = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                enquiry = paginator.page(paginator.num_pages)

            next_page_number = 1
            has_next_page = False
            if enquiry.has_next():
                has_next_page = True
                next_page_number = enquiry.next_page_number()

            has_previous_page = False
            previous_page_number = 1
            if enquiry.has_previous():
                has_previous_page = True
                previous_page_number = enquiry.previous_page_number()

            serialized_data = EnquiryListSerializer(
                enquiry,
                context = {
                    "request" : request
                },
                many=True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data,
                "pagination_data" : {
                    'current_page': enquiry.number,
                    'has_next_page': has_next_page,
                    'next_page_number': next_page_number,
                    'has_previous_page': has_previous_page,
                    'previous_page_number': previous_page_number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'first_item': enquiry.start_index(),
                    'last_item': enquiry.end_index(),
                },
            }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Enquiry not found"
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
@permission_classes([AllowAny,])
def create_enquiry(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateEnquirySerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            phone = request.data["phone"]
            email = request.data["email"]
            message = request.data["message"]

            if not Enquiry.objects.filter(name=name, phone=phone, email=email, message=message).exists():
                enquiry = Enquiry.objects.create(
                    auto_id = get_auto_id(Enquiry),
                    name = name,
                    phone = phone,
                    email = email,
                    message = message
                )

                subject = "English Cafe Enquiry Data"
                content = "Enquiry user details"

                host_email = settings.EMAIL_HOST_USER
                context = {
                    "request" : request,
                    'email' : email,
                    'name' :name,
                    'phone' : phone,
                    'email' : email,
                    "message" : message,
                    "subject" : subject,
                    "content" : content,
                    'mail_title' : "Enquiry Details",
                }
                template_name = 'enquiry.html'
                html_content = render_to_string(template_name, context)
                try:
                    send_emails(host_email, subject, content, html_content)
                except Exception as e:
                    print(str(e),"-=-=-=-=-")

                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Enquiry submitted successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Already you have submitted the enquiry"
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
def add_company_profile_count(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddCompanyCountSerializer(data=request.data)
        if serialized_data.is_valid():
            successfull_students = request.data["successfull_students"]
            languages_trainee = request.data["languages_trainee"]
            awards_won = request.data["awards_won"]
            courses = request.data["courses"]

            max_instances = 1

            instance_count = CompanyCount.objects.count()

            if not instance_count >= max_instances:
                comapny_count = CompanyCount.objects.create(
                    auto_id = get_auto_id(CompanyCount),
                    successfull_students = successfull_students,
                    languages_trainee = languages_trainee,
                    awards_won = awards_won,
                    courses = courses
                )

                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Company profile count created successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Input already exists. You can only edit the existing input"
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
@group_required(['Student', 'EnglishCafe'])
def get_company_profile_count(request):
    try:
        transaction.set_autocommit(False)
        if (company_counts := CompanyCount.objects.filter(is_deleted=False)).exists():
            company_counts = company_counts.latest("date_added")
            serialized_data = CompanyCountListSerializer(
                company_counts,
                context = {
                    "request" : request,
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
                    "message" : "Company count not found"
                }
            }
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
def edit_company_profile_count(request, pk):
    try:
        transaction.set_autocommit(False)
        successfull_students = request.data.get("successfull_students")
        languages_trainee = request.data.get("languages_trainee")
        awards_won = request.data.get("awards_won")
        courses = request.data.get("courses")

        if (company_profile_count := CompanyCount.objects.filter(pk=pk, is_deleted=False)).exists():
            company_profile_count = company_profile_count.latest("date_added")

            if successfull_students:
                company_profile_count.successfull_students = successfull_students
            if languages_trainee:
                company_profile_count.languages_trainee = languages_trainee
            if awards_won:
                company_profile_count.awards_won = awards_won
            if courses:
                company_profile_count.courses = courses
            company_profile_count.save()
            
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Company count edit completed successfully"
                }
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Company count not found"
                }
            }
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

    


    

    









    
