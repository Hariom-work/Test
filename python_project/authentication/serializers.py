from rest_framework import serializers
from . import models

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields =[
            'id', 'first_name', 'last_name','username', 'email',"date_joined"
        ]