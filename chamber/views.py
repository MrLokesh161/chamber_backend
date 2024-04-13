from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import Form1Serializer, DirectorSerializer, Form2Serializer, EventsSerializer, ContactSerializer
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Form1 as Form1Model, PaymentTransaction, MembershipPrices, Events, Contact
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
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
def get_user_information(request):
    users_data = []
    
    users = User.objects.all()
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'form1_data': None,
            'payment_transaction_data': None
        }
        
        try:
            form1_instance = Form1Model.objects.get(user=user)
            user_data['form1_data'] = {
                'Nameofapplicant': form1_instance.Nameofapplicant,
                'Businessactivity': form1_instance.Businessactivity,
                'cdlan': form1_instance.cdlan,
                'cdphone': form1_instance.cdphone,
                'cdemail': form1_instance.cdemail,
                'cdweb': form1_instance.cdweb,
                'constitution': form1_instance.constitution,
                'regoffadd': form1_instance.regoffadd,
                'acoffice': form1_instance.acoffice,
                'acwork': form1_instance.acwork,
            }
        except Form1Model.DoesNotExist:
            user_data['form1_data'] = None
            
        try:
            payment_transaction_instance = PaymentTransaction.objects.get(user=user)
            user_data['payment_transaction_data'] = {
                'membership_type': payment_transaction_instance.membership_type,
                'sales_turnover': payment_transaction_instance.sales_turnover,
                'registration_date': payment_transaction_instance.registration_date,
                'membership_expiry_date': payment_transaction_instance.membership_expiry_date,
            }
        except PaymentTransaction.DoesNotExist:
            user_data['payment_transaction_data'] = None
            
        users_data.append(user_data)
    
    return Response(users_data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    if request.method == 'POST':
        membership_type = request.data.get('membership_type')
        sales_turnover = request.data.get('sales_turnover')
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')
        cardholder_name = request.data.get('cardholder_name')
        journal_subscription = request.data.get('journal_subscription', False)
        chamber_day_celebrations = request.data.get('chamber_day_celebrations', False)

        total_amount = calculate_total_amount(membership_type, sales_turnover, journal_subscription, chamber_day_celebrations)
        entrance_fee = getattr(MembershipPrices, 'admissionFee', 0)
        selected_membership_amount = total_amount - entrance_fee

        Membership_expiry_date = None  # Initialize the variable outside the if block

        if membership_type != 'life':
            current_date = datetime.now()
            Membership_expiry_date = current_date + timedelta(days=365)  # Assign value conditionally

        user = request.user
        print(user)

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

        return Response({'message': 'Payment successful!', 'Membership_expiry_date': Membership_expiry_date}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_view(request):
    events = Events.objects.all()
    serializer = EventsSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def formadmin_view(request):
    form1 = Form1Model.objects.all()
    serializer = Form1Serializer(form1, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contact_view(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Details": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def test_token(request):
    return Response({})

