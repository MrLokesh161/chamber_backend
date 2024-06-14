# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model  
from .models import Form1, Director, Form2, Events, Contact, PaymentTransaction, Certificate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username','email', 'password') 

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class Form2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Form2
        fields = '__all__'

class Form1Serializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)
    Form2 = Form2Serializer(many=True, read_only=True)

    class Meta:
        model = Form1
        fields = '__all__' 

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'Eventimage', 'NameofEvent', 'Description', 'DateofEvent', 'LinkforEvent']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class DateFieldTZ(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value is None:
            return None
        return value.date()

class MembersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    registration_date = DateFieldTZ()  # Remove the source parameter # Use custom DateFieldTZ
    class Meta:
        model = PaymentTransaction
        fields = ['username', 'registration_date']


class Form1ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form1
        fields = '__all__'

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if value is not None:
                setattr(instance, field, value)
        instance.save()
        return instance
    
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'