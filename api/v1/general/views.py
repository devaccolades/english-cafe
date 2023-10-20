import traceback
import os

from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from general.models import Blog
from api.v1.general.serializers import ListBlogSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def list_blogs(request):
    try:
        if (blogs := Blog.objects.filter(is_deleted=False)).exists():

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
