from rest_framework.views import APIView
from core.response import Response
from .import serializers
from . import validators
from core.exceptions import SerializerError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from . import validators
from . import serializers
from . import models

# Create your views here.
class Projects(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {
            "success": 1,
            "message": "Project created successful",
            "data": {},
        }
        try:
            req_body = request.data
            validator = validators.ProjectValidator(data=req_body)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            req_params = validator.validated_data
            models.Project.objects.create(owner = request.user,**req_params)
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def get(self, request):
        context = {
            "success": 1,
            "message": "Project data",
            "data": {},
        }
        try:
            project_obj = models.Project.objects.filter(is_active=True)
            serializer = serializers.ProjectSerializer(project_obj, many=True)
            if not serializer.data:
                raise Exception("No data found")
            context['data']=serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

    
class Project(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        context = {
            "success": 1,
            "message": 'Project details fetched successfully.',
            "data": {}
        }
        try:
            project_details = models.Project.objects.filter(is_active=True,id=id).first()
            serializer = serializers.ProjectSerializer(project_details)
            context['data'] = serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    

    def put(self, request, id):
        context = {
            "success": 1,
            "message": "Project data updated successfully.",
            "data": {}
        }
        try:
            req_data = request.data
            validator = validators.ProjectValidator(data=req_data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            project = models.Project.objects.filter(is_active=True,id=id).first()
            if not project:
                raise Exception("Data not found")
            for attr, value in validator.validated_data.items():
                setattr(project, attr, value)
            project.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def delete(self, request, id):
        context = {
            "success": 1,
            "message": "Project deleted successfully.",
            "data": {}
        }
        try:
            Project = models.Project.objects.filter(is_active=True, id=id).first()
            if not Project:
                raise Exception("Project does not exist")
            Project.is_active=False
            Project.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)


class Tasks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {
            "success": 1,
            "message": "Task created successful",
            "data": {},
        }
        try:
            req_body = request.data
            validator = validators.TaskValidator(data=req_body)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            req_params = validator.validated_data
            if "assign_to" in req_params:
                req_params["assign_to"]=models.CustomUser.objects.get(id=req_params["assign_to"])
            req_params["project"]=models.Project.objects.get(id=id)
            models.Task.objects.create(**req_params)
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def get(self, request,id):
        context = {
            "success": 1,
            "message": "Project Tasks",
            "data": {},
        }
        try:
            project_obj = models.Task.objects.filter(is_active=True, project__id=id)
            serializer = serializers.TaskSerializer(project_obj, many=True)
            if not serializer.data:
                raise Exception("No data found")
            context['data']=serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

    
class Task(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        context = {
            "success": 1,
            "message": 'Task details fetched successfully.',
            "data": {}
        }
        try:
            task_details = models.Task.objects.filter(is_active=True,id=id).first()
            serializer = serializers.TaskSerializer(task_details)
            context['data'] = serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    

    def put(self, request, id):
        context = {
            "success": 1,
            "message": "Task data updated successfully.",
            "data": {}
        }
        try:
            req_data = request.data
            validator = validators.TaskValidator(data=req_data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            task = models.Task.objects.filter(is_active=True,id=id).first()
            if not task:
                raise Exception("Data not found")
            for attr, value in validator.validated_data.items():
                setattr(task, attr, value)
            task.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def delete(self, request, id):
        context = {
            "success": 1,
            "message": "Project deleted successfully.",
            "data": {}
        }
        try:
            task = models.Task.objects.filter(is_active=True, id=id).first()
            if not task:
                raise Exception("Task does not exist")
            task.is_active=False
            task.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    

class Comments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {
            "success": 1,
            "message": "Added comment on task successfully",
            "data": {},
        }
        try:
            req_body = request.data
            validator = validators.CommentValidator(data=req_body)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            req_params = validator.validated_data
            req_params["user"]=request.user
            req_params["task"]=models.Task.objects.get(id=id)
            models.Comment.objects.create(**req_params)
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def get(self, request,id):
        context = {
            "success": 1,
            "message": "Tasks comments",
            "data": {},
        }
        try:
            req_body = request.data
            project_obj = models.Comment.objects.filter(is_active=True, task__id=id)
            serializer = serializers.CommentSerializer(project_obj, many=True)
            if not serializer.data:
                raise Exception("No data found")
            context['data']=serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

    
class Comment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        context = {
            "success": 1,
            "message": 'Comment details fetched successfully.',
            "data": {}
        }
        try:
            comment = models.Comment.objects.filter(is_active=True,id=id).first()
            serializer = serializers.CommentSerializer(comment)
            context['data'] = serializer.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    

    def put(self, request, id):
        context = {
            "success": 1,
            "message": "Comment data updated successfully.",
            "data": {}
        }
        try:
            req_data = request.data
            validator = validators.CommentValidator(data=req_data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            comment = models.Comment.objects.filter(is_active=True,id=id).first()
            if not comment:
                raise Exception("Data not found")
            for attr, value in validator.validated_data.items():
                setattr(comment, attr, value)
            comment.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
    def delete(self, request, id):
        context = {
            "success": 1,
            "message": "Comment deleted successfully.",
            "data": {}
        }
        try:
            comment = models.Comment.objects.filter(is_active=True, id=id).first()
            if not comment:
                raise Exception("Comment does not exist")
            comment.is_active=False
            comment.save() 
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)