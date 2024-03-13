from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
# from .serializers import Form1Serializer, DirectorSerializer, Form2Serializer
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib import messages
# from .models import Form1 as Form1Model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def signupview(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_form1(request):
    if request.method == 'POST':
        serializer = Form1Serializer(data=request.data)
        print(request.data['is_individual'])
        if request.data['constitution']=='Individual':
            request.data['is_individual']=True
        

        if serializer.is_valid():
            directors_data = request.data.get('directors')

            form1_instance = serializer.save()

            if directors_data:
                director_serializer = DirectorSerializer(data=directors_data, many=True)
                if director_serializer.is_valid():
                    directors = director_serializer.save()
                    form1_instance.directors.set(directors)

            response_data = {
                'detail': 'Success',
                'pk': form1_instance.pk,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        print(request.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
@api_view(['POST'])
def create_form2(request, form1_instance_id):
    if request.method == 'POST':
        form1_instance = get_object_or_404(Form1Model, id=form1_instance_id)
        

        form2_serializer = Form2Serializer(data=request.data, context={'form1_instance': form1_instance})
        if form2_serializer.is_valid():
            form2_instance = form2_serializer.save()
            
            form1_instance.Form2.add(form2_instance)

            messages.success(request, 'Form 2 submitted successfully.')
            return Response({"Form2": "Success"}, status=status.HTTP_201_CREATED)

        return Response(form2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(['POST'])
# # def loginview(request):
# #     if request.method == 'POST':
# #         Emailid = request.data.get('Emailid')
# #         password = request.data.get('password')
# #         print(Emailid,password)
# #         try:
# #             user = User.objects.get(Emailid=Emailid, password=password)
# #             if user:
# #                 return Response({"login" : "Success"})
# #             else: 
# #                 return Response({"login": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
# #         except:
# #             return Response({"login": "Invalid Credentials"})
        

# # @api_view(['POST'])
# # def signupview(request):
# #     if request.method == 'POST':
# #         data = request.data
# #         username = data.get('username')
# #         Emailid = data.get('Emailid')
# #         mobilenum = data.get('mobilenum')
# #         password = data.get('password')

# #         if username and password and Emailid and mobilenum:
# #             if User.objects.filter(Emailid=Emailid).exists():
# #                 return Response({'error': 'User with this email already exists.'}, status=400)
# #             elif User.objects.filter(mobilenum=mobilenum).exists():
# #                 return Response({'error': 'User with this phone number already exists.'}, status=400)
            
# #             user = User(
# #                 username=username,
# #                 Emailid=Emailid,
# #                 mobilenum=mobilenum,
# #                 password=password
# #             )
# #             user.save()
# #             return Response({'success': 'User created successfully.'}, status=201)

# #         return Response({'error': 'Email and password are required fields.'}, status=400)

# #     return Response({'error': 'Invalid request method.'}, status=400)


@api_view(['GET'])
def test_token(request):
    return Response({})