from rest_framework import serializers
from .models import Contact, UserContactMapping, UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class UserContactMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContactMapping
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
