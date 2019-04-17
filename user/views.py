from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from user.serializers import UserSerializer,MovieSerializer
from user.models import User,Movie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#login API for user login with token genration(DRF)
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

#logout API for user logout 
class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response("You have successfully logged out!",status=status.HTTP_200_OK)

#user sign up/registration API
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response("You have successfully created user!",status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



# Movies CRUD
class MovieView(APIView):
	
	def post(self,request):
		try:
			movie_data = MovieSerializer(data=request.data)
			if not(movie_data.is_valid()):
				return Response(movie_data.errors)
			movie_data.save()
			return Response("Movie created successfully",status=status.HTTP_201_CREATED)
		except Exception as err:
			print(err)
			return Response("Error while creating Movie")

	def get(self,request,movie_id=None):
		try:
			if(movie_id):
				movie_data = Movie.objects.filter(pk=movie_id,is_deleted = False)[0]
				get_data = MovieSerializer(movie_data)
			else:
				movie_data = Movie.objects.filter(is_deleted = False)
				get_data = MovieSerializer(movie_data,many=True)
			return Response(get_data.data,status=status.HTTP_200_OK)
		except Exception as err: 
			print(err) 
			return Response("Error while getting details")


	def put(self,request,movie_id):
		try:
			get_data = Movie.objects.get(pk=movie_id)
			update_data = MovieSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return Response("Movie details updated Successfully")
			else:
				return Response(update_data.errors)	
		except:
			return Response("Error while updating details")

	def delete(self,request,movie_id):
		try:
			Movie.objects.filter(pk=movie_id).update(is_deleted = True)
			return Response("Movie Deleted Successfully",status=status.HTTP_200_OK)
		except Exception as err:
			print(err)    
			return Response("Error while deleting the Movie",500)
