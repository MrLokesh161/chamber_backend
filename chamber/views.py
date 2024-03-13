from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import Form1Serializer, DirectorSerializer, Form2Serializer
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Form1 as Form1Model, PaymentTransaction, MembershipPrices
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy
from datetime import datetime, timedelta
from .utils import calculate_total_amount

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'login': 'Success'
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
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_form1(request):
    if request.method == 'POST':
        user = request.user 

        # Create a mutable copy of request.data
        mutable_data = request.data.copy()

        # Update the mutable copy with user information
        mutable_data['user'] = user.pk

        serializer = Form1Serializer(data=mutable_data)
        print(mutable_data['is_individual'])
        if mutable_data['constitution'] == 'Individual':
            mutable_data['is_individual'] = True

        if serializer.is_valid():
            directors_data = mutable_data.get('directors')

            print(serializer)

            form1_instance = serializer.save()

            print(form1_instance)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_form2(request):
    if request.method == 'POST':
        form1_instance = get_object_or_404(Form1Model, user=request.user)

        form2_serializer = Form2Serializer(data=request.data, context={'form1_instance': form1_instance})
        if form2_serializer.is_valid():
            form2_instance = form2_serializer.save()

            form1_instance.Form2.add(form2_instance)

            messages.success(request, 'Form 2 submitted successfully.')
            return Response({"Form2": "Success"}, status=status.HTTP_201_CREATED)

        return Response(form2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_page_view(request):
    if request.method == 'GET':
        try:
            # Assuming 'user' is the correct field name in your Form1Model model
            form1_instance = Form1Model.objects.get(user=request.user)
            print(request.user.username)

            
            user_info = {
                'name': request.user.username,
                'email': request.user.email,
                'business_activity': form1_instance.Businessactivity,
            }
            print(user_info)

            return Response(user_info, status=status.HTTP_200_OK)
        except Form1Model.DoesNotExist:
            return Response({'error': 'User information not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    if request.method == 'POST':
        # Extract data from the request
        membership_type = request.data.get('membership_type')
        sales_turnover = request.data.get('sales_turnover')
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')
        cardholder_name = request.data.get('cardholder_name')
        journal_subscription = request.data.get('journal_subscription', False)
        chamber_day_celebrations = request.data.get('chamber_day_celebrations', False)

        # Calculate the total amount and set other fields accordingly
        total_amount = calculate_total_amount(membership_type, sales_turnover, journal_subscription, chamber_day_celebrations)
        entrance_fee = getattr(MembershipPrices, 'admissionFee', 0)
        selected_membership_amount = total_amount - entrance_fee

        # Calculate membership expiry based on membership type
        if membership_type == 'life':
            expiry_date = None  # Set to None for lifetime membership
        else:
            current_date = datetime.now()
            Membership_expiry_date = current_date + timedelta(days=365)  # Membership valid for one year

        # Get the user associated with the authentication token
        user = request.user

        # Create a PaymentTransaction instance associated with the user
        payment_transaction = PaymentTransaction.objects.create(
            user=user,
            membership_type=membership_type,
            sales_turnover=sales_turnover,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            cardholder_name=cardholder_name,
            entrance_fee=entrance_fee,
            selected_membership_amount=selected_membership_amount,
            journal_subscription=journal_subscription,
            chamber_day_celebrations=chamber_day_celebrations,
            total_amount=total_amount,
            membership_expiry_date=Membership_expiry_date,
        )

        # You can add additional logic here, like sending confirmation emails, etc.

        return Response({'message': 'Payment successful!', 'Membership_expiry_date': Membership_expiry_date}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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