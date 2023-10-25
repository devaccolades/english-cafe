import traceback
import os

from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from general.models import Blog, Tags
from api.v1.general.serializers import ListBlogSerializer, ListTagsSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def list_blogs(request):
    try:
        if (blogs := Blog.objects.filter(is_deleted=False)).exists():
            blogs = blogs.order_by("-date_added")

            serialized_data = ListBlogSerializer(
                blogs,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode": 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }

        transaction.set_autocommit(False)
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
@permission_classes([AllowAny])
def single_blog(request, slug):
    try:
        if (blogs := Blog.objects.filter(slug=slug, is_deleted=False)).exists():
            blog = blogs.latest('date_added')

            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request" : request
                },
            ).data

            response_data = {
                "StatusCode": 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }

        transaction.set_autocommit(False)
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
@permission_classes([AllowAny])
def list_tags(request):
    try:
        if (tags := Tags.objects.filter(is_deleted=False)).exists():
            tags = tags.order_by("-date_added")

            serialized_data = ListTagsSerializer(
                tags,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode": 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }

        transaction.set_autocommit(False)
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
@permission_classes([AllowAny])
def list_blogs_tags(request, pk):
    try:
        if (tags := Tags.objects.filter(pk=pk, is_deleted=False)).exists():
            tags = tags.latest("date_added")
            
            if (blogs := Blog.objects.filter(tags=tags, is_deleted=False)).exists():
                blogs = blogs.order_by("-date_added")

                serialized_data = ListBlogSerializer(
                    blogs,
                    context = {
                        "request" : request
                    },
                    many = True
                ).data

                response_data = {
                    "StatusCode": 6000,
                    "data" : serialized_data
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : []
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "Tags not found"
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

