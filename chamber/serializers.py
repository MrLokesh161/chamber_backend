# serializers.py
from rest_framework import serializers
from .models import Form1, Director

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class Form1Serializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Form1
        fields = '__all__'

