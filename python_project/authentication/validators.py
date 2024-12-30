from rest_framework import serializers
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password(password):
    if not 8 <= len(password) <= 15:
        raise ValidationError(_('Password must be between 8 and 20 characters long.'), code='password_length')

    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    if not re.match(password_regex, password):
        raise ValidationError(_('Password must contain at least one lowercase letter, one uppercase letter, one number, and one special character.'), code='password_complexity')

class UserRegisterValidator(serializers.Serializer):

    # fields
    email = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': 'Email is required',
        'blank': 'Email field cannot be empty',
    })
    password = serializers.CharField(max_length=20, required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Password is required field',
        'null': 'password cannot be null',
        'blank': 'Password field cannot be empty'
    },validators=[validate_password])
    first_name = serializers.CharField(max_length=100, required=True, allow_blank=False, error_messages={
        'required': 'First Name is a required field.',
        'blank': 'First Name field cannot be empty.',
    })
    last_name = serializers.CharField(max_length=100, required=True, allow_blank=False, error_messages={
        'required': 'Last Name is a required field.',
        'blank': 'Last Name field cannot be empty.',
    })
    username = serializers.CharField(max_length=100, required=True, allow_blank=False, error_messages={
        'required': 'User Name is a required field.',
        'blank': 'User Name field cannot be empty.',
    })

class UserLoginValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Email is required field',
        'null': 'email cannot be null',
        'blank': 'Email field cannot be empty'
    })
    password = serializers.CharField(max_length=20, required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Password is required field',
        'null': 'password cannot be null',
        'blank': 'Password field cannot be empty'
    },validators=[validate_password])
    
class ProfileUpdateValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date_joined = serializers.DateField(required=False, allow_null=True)
