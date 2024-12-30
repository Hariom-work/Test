from rest_framework import serializers
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProjectValidator(serializers.Serializer):

    # # fields
    # owner = serializers.CharField(max_length=50, required=True, allow_blank=False, error_messages={
    #     'required': 'Owner is required',
    #     'blank': 'Owner field cannot be empty',
    # })
    name = serializers.CharField(max_length=50, required=True, allow_null=False, error_messages={
        'required': 'Project name is required field',
        'blank': 'Project name field cannot be empty'
    })
    description = serializers.CharField(max_length=500, required=True, allow_blank=False, error_messages={
        'required': 'Project description is a required field.',
        'blank': 'Project description field cannot be empty.',
    })


class CommentValidator(serializers.Serializer):
    content = serializers.CharField(max_length=500, required=True, allow_blank=False, error_messages={
        'required': 'Content is required',
        'blank': 'Content field cannot be empty',
    })

class TaskValidator(serializers.Serializer):

    # # fields
    assign_to = serializers.CharField(max_length=50, required=False, allow_blank=True)
    # project = serializers.CharField(max_length=50, required=True, allow_blank=False, error_messages={
    #     'required': 'Project is required',
    #     'blank': 'Project field cannot be empty',
    # })
    title = serializers.CharField(max_length=50, required=True, allow_null=False, error_messages={
        'required': 'Task title is required field',
        'blank': 'Task title field cannot be empty'
    })
    status = serializers.CharField(max_length=50, required=True, allow_null=False, error_messages={
        'required': 'Task status is required field',
        'blank': 'Task status field cannot be empty'
    })
    priority = serializers.CharField(max_length=50, required=True, allow_null=False, error_messages={
        'required': 'Task priority is required field',
        'blank': 'Task priority field cannot be empty'
    })
    description = serializers.CharField(max_length=500, required=True, allow_blank=False, error_messages={
        'required': 'Task description is a required field.',
        'blank': 'Task description field cannot be empty.',
    })
    due_date = serializers.DateField(required=True, allow_null=False,error_messages={
        'required': 'Task due date is a required field.',
        'blank': 'Task due date field cannot be empty.',
    })


