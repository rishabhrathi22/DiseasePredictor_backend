from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status

from . import handleDb
from .serializers import UserSerializer

class UserViewSet(viewsets.ViewSet):
	"""
	A simple ViewSet for registering users.
	"""

	serializer_class = UserSerializer

	def register(self, request):
		serializer = UserSerializer(data=request.data)

		if serializer.is_valid() and handleDb.addUser(request.data):
			return Response("Student Registered Successfully", status = status.HTTP_201_CREATED)

		return Response("Unable to register", status = status.HTTP_400_BAD_REQUEST)

"""
{
	"email": "abcd@gmail.com",
	"uid": "gvewhbdft67er3b2"
}
"""