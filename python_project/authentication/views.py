from rest_framework.views import APIView
from core.response import Response
from .import serializers
from . import validators
from core.exceptions import SerializerError
from django.contrib.auth import authenticate, login
from core import general
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import models
from django.db.models import Q

class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {
            "success": 1,
            "message": "User logged in successfully",
            "data": {}
        }
        try:
            # Validate the input
            validator = validators.UserLoginValidator(data=request.data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)

            # Authenticate the user
            req_params = validator.validated_data
            auth_user = authenticate(request, username=req_params['email'], password=req_params['password'])
            print("Authenticated user:", auth_user)

            # Check if the user is authenticated
            if auth_user is not None:
                if not auth_user.is_active:
                    context['success'] = 0
                    context['message'] = "This account is inactive."
                    return Response(context, status=status.HTTP_403_FORBIDDEN)
                else:
                    context['message'] = "logged in successfully"
                # Log the user in and generate tokens
                login(request, auth_user)
                tokens = general.get_tokens_for_user(auth_user)
                context['data'] = { **tokens }

            else:
                context['success'] = 0
                context['message'] = "Invalid credentials"
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        return Response(context)


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {
            "success": 1,
            "message": "User created successful",
            "data": {},
        }
        try:
            req_body = request.data
            validator = validators.UserRegisterValidator(data=req_body)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            req_params = validator.validated_data
            email_exist_check = models.CustomUser.objects.filter(Q(email=req_params['email']) | Q(username=req_params['username'])).first()
            if email_exist_check:
                raise Exception("This email or username has already been taken, please login.")           
            models.CustomUser.objects.create_user(**req_params)
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        context = {
            "success": 1,
            "message": 'Profile details fetched successfully.',
            "data": {}
        }
        try:
            user_details = models.CustomUser.objects.filter(id=id).first()
            serializer = serializers.UserProfileSerializer( user_details)
            context['data'] = serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    

    def put(self, request, id):
        context = {
            "success": 1,
            "message": "User data updated successfully.",
            "data": {}
        }
        try:
            req_data = request.data
            validator = validators.ProfileUpdateValidator(data=req_data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            user = models.CustomUser.objects.filter(id=id).first()
            if not user:
                raise Exception("Could not update the profile information, please try later.")
            for attr, value in validator.validated_data.items():
                setattr(user, attr, value)
            user.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def delete(self, request, id):
        context = {
            "success": 1,
            "message": "User deleted successfully.",
            "data": {}
        }
        try:
            user = models.CustomUser.objects.filter(id=id).first()
            if not user:
                raise Exception("User does not exist")
            user.is_active=False
            user.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)