from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import Form1Serializer, DirectorSerializer, Form2Serializer, EventsSerializer, ContactSerializer, MembersSerializer, Form1ModelSerializer
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404, render
from django.forms.models import model_to_dict
from django.http import JsonResponse
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token(request):
    return Response({'message': 'Token is valid'})

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
    
    # Get the authenticated user
    user = request.user
    
    # Get the token of the authenticated user
    
    users = User.objects.all()
    for user in users:
        token = Token.objects.get(user=user).key
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'form1_data': None,
            'payment_transaction_data': None,
            'token': token  
        }
        
        try:
            form1_instance = Form1Model.objects.get(user=user)
            user_data['form1_data'] = {
                'Nameofapplicant': form1_instance.Nameofapplicant,
                'Businessactivity': form1_instance.Businessactivity,
                'regoffadd': form1_instance.regoffadd,
                'acoffice': form1_instance.acoffice,
                'acwork': form1_instance.acwork,
                'cdlan': form1_instance.cdlan,
                'cdphone': form1_instance.cdphone,
                'cdemail': form1_instance.cdemail,
                'cdweb': form1_instance.cdweb,
                'aadhar': form1_instance.aadhar,
                'pancardno': form1_instance.pancardno,
                'GSTNo': form1_instance.GSTNo,
                'CompanyFirmRegNo': form1_instance.CompanyFirmRegNo,
                'SocietyAssociationRegNo': form1_instance.SocietyAssociationRegNo,
                'paname': form1_instance.paname,
                'papan': form1_instance.papan,
                'paphone': form1_instance.paphone,
                'padesignation': form1_instance.padesignation,
                'paaadhaar': form1_instance.paaadhaar,
                'pamail_id': form1_instance.pamail_id,
                'indmain_category': form1_instance.indmain_category,
                'indsub_category': form1_instance.indsub_category,
                'cmdomestic': form1_instance.cmdomestic,
                'cmboth': form1_instance.cmboth,
                'cmpercentage_of_imports': form1_instance.cmpercentage_of_imports,
                'cmglobal_market': form1_instance.cmglobal_market,
                'cmpercentage_of_exports': form1_instance.cmpercentage_of_exports,
                'country_name_foreign_collaboration': form1_instance.country_name_foreign_collaboration,
                'collaborator_name_foreign_collaboration': form1_instance.collaborator_name_foreign_collaboration,
                'annual_turnover_year1': form1_instance.annual_turnover_year1,
                'annual_turnover_year2': form1_instance.annual_turnover_year2,
                'annual_turnover_year3': form1_instance.annual_turnover_year3,
                'classindustry': form1_instance.classindustry,
                'direct_office_employees': form1_instance.direct_office_employees,
                'indirect_contractual_employees': form1_instance.indirect_contractual_employees,
                'works_employees': form1_instance.works_employees,
                'outsourced_employees': form1_instance.outsourced_employees,
                'esic': form1_instance.esic,
                'epf': form1_instance.epf,
                'branches_outside_india': form1_instance.branches_outside_india,
                'is_member_of_association': form1_instance.is_member_of_association,
                'association_name': form1_instance.association_name,
                'is_office_bearer': form1_instance.is_office_bearer,
                'association_position': form1_instance.association_position,
                'reason_for_joining_chamber': form1_instance.reason_for_joining_chamber,
                'form_status': form1_instance.form_status,
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_payment(request):
    if request.method == 'POST':
        membership_type = request.data.get('membership_type')
        sales_turnover = request.data.get('sales_turnover')
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')
        cardholder_name = request.data.get('cardholder_name')

        # Calculate total amount based on membership type and sales turnover
        total_amount = calculate_total_amount(membership_type, sales_turnover)

        # Set entrance fee and selected membership amount based on membership type
        if membership_type == 'life':
            total_amount = 88500  # Lifetime membership fee
            entrance_fee = 0  # No entrance fee for lifetime membership
            selected_membership_amount = total_amount
        else:
            entrance_fee = 3540  # Entrance fee for non-lifetime membership
            selected_membership_amount = total_amount - entrance_fee

        # Calculate expiry date for non-lifetime memberships
        membership_expiry_date = None
        if membership_type != 'life':
            current_date = datetime.now()
            membership_expiry_date = current_date + timedelta(days=365)

        # Get the authenticated user
        user = request.user

        # Create payment transaction instance
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
            total_amount=total_amount,
            membership_expiry_date=membership_expiry_date,
        )

        # Return response
        return Response({'message': 'Payment successful!', 'Membership_expiry_date': membership_expiry_date}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_view(request):
    events = Events.objects.all()
    serializer = EventsSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MembersView(request):
    events = PaymentTransaction.objects.all()
    serializer = MembersSerializer(events, many=True)
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
@permission_classes([IsAuthenticated])
def test_token(request):

    users_data = []
    
    # Get the authenticated user
    user = request.user
    
    # Get the token of the authenticated user
    
    users = User.objects.all()
    for user in users:
        token = Token.objects.get(user=user).key
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token  
        }

        users_data.append(user_data)
    
    return Response(users_data)



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ApproveApplicaton(request):

    
    if request.method == 'GET':
        # Retrieve all forms
        forms = Form1Model.objects.all()
        serializer = Form1Serializer(forms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        form_id = request.data.get('id')
        status_process = request.data.get('status')
        print("Status Process:", status_process)  # Print the received status for debugging
        if not form_id or status_process not in ['approve', 'reject', 'payment successful']:  # Updated condition
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the form
        form = Form1Model.objects.filter(pk=form_id).first()
        if not form:
            return Response({'error': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

        # Perform status transition based on the current status and action
        if status_process == 'approve':
            if form.form_status == 'pending':
                form.form_status = 'Approved by AO'
            elif form.form_status == 'Approved by AO':
                form.form_status = 'Approved by CEO'
            elif form.form_status == 'Approved by CEO':
                form.form_status = 'Approved by Membership Committee'
            elif form.form_status == 'Approved by Membership Committee':
                form.form_status = 'Approved by OB'
            elif form.form_status == 'Approved by OB':
                form.form_status = 'waiting for payment'
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)
        elif status_process == 'payment successful':  # Updated condition
            form.form_status = 'Payment done (approved as Member)'  # Update status directly
        elif status_process == 'reject':
            form.form_status = 'rejected'
            rejection_reason = request.data.get('ror')
            if not rejection_reason:
                return Response({'error': 'Rejection reason required'}, status=status.HTTP_400_BAD_REQUEST)
            form.ror = rejection_reason
        else:
            return Response({'error': 'Invalid status action'}, status=status.HTTP_400_BAD_REQUEST)
         
        # Save the updated form status
        form.save()

        # Prepare response
        cont = {'message': 'Form status updated successfully'}
        if form.form_status == 'rejected':
            cont['message'] = 'Form rejected'
        cont['content'] = Form1Serializer(form).data
        
        return Response(cont, status=status.HTTP_200_OK)








@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def singleApplication(request,id):
    if request.method == 'GET':
        form = Form1Model.objects.get(pk=id)
        serializer = Form1Serializer(form)
        cont ={
            'content': serializer.data,
            'message': 'Success'
        }
        return Response(cont) 



@api_view(['GET', 'POST'])
def form1_detail(request, pk):
    try:
        form1_instance = Form1Model.objects.get(pk=pk)
    except Form1Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        form1_data = model_to_dict(form1_instance)
        # Filter out any binary fields
        form1_data_filtered = {key: value for key, value in form1_data.items() if not isinstance(value, bytes)}
        return Response(form1_data_filtered)
    
    elif request.method == 'POST':
        serializer = Form1ModelSerializer(instance=form1_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ExistingMembercheck (request):

    if request.method == 'GET':
        # Retrieve all forms
        forms = Form1Model.objects.all()
        serializer = Form1Serializer(forms, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        
        serializer = Form1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({})


def home_page(request):
    return render(request, 'index.html')