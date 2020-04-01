from django.shortcuts import render
from pytz import unicode
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request):
    content = {
        'user': unicode(request.user),
        'auth': unicode(request.auth),
    }

    return Response(content)
