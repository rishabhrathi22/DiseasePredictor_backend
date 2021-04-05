from django.shortcuts import render
from django.http import HttpResponse
from . import handleDb

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .serializers import UserSerializer

class UserViewSet(viewsets.ViewSet):
	"""
	A simple ViewSet for registering users.
	"""

	serializer_class = UserSerializer

	def register(self, request):
		if (handleDb.addUser(request.data)):
			return Response(request.data, status = status.HTTP_201_CREATED)

		return Response("Unable to register.", status = status.HTTP_400_BAD_REQUEST)