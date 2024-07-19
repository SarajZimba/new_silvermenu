from user.models import Customer, CustomerNormalLogin, CustomerGoogleLogin
from rest_framework.views import APIView
from api.serializers.customer import CustomerSerializer
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from user.utils import check_email, check_email_in_normal


class CustomerNormalRegister(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        print(data)
        email = data.get('email')
        username = data.get('name')
        check_email = check_email(email) # check if email is already associated with another account
        if check_email == True:
            return Response({"data":"Email already associated with another account"}, 400)
        password = data.pop('password')
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            customer = serializer.save()

        customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        customerNormallogin.set_password(password)
        customerNormallogin.save()
        return Response({"data":"Customer Registered successfully"}, 200)
    
class CustomerGoogleRegister(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        email = data.get('email')
        username = data.get('name')
        check_email = check_email_in_normal(email)  # check if email is already associated with another account

        if CustomerGoogleLogin.objects.filter(email=email).exists():
            customer_googlelogin = CustomerGoogleLogin.objects.filter(email=email).first()
            customer = customer_googlelogin.customer
            response_data = {'customer' : {
                'username': customer.name,
                'email': customer.email,
                'id': customer.id,
                'email': customer.email,
                'contact_number': customer.phone,
                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            if check_email == True:
                password = data.pop('password')
                customer = Customer.objects.get(email=email)
                customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
                customerGooglelogin.set_password(password)
                customerGooglelogin.save()
                response_data = {'customer' : {
                    'username': customer.name,
                    'email': customer.email,
                    'id': customer.id,
                    'email': customer.email,
                    'contact_number': customer.phone,
                    # Add any other customer details you want to include
                }}
                return Response(response_data, 200)
            else:
                password = data.pop('password')
                serializer = CustomerSerializer(data=data)
                if serializer.is_valid():
                    customer = serializer.save()

                customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
                customerGooglelogin.set_password(password)
                customerGooglelogin.save()
                response_data = {'customer' : {
                    'username': customer.name,
                    'email': customer.email,
                    'id': customer.id,
                    'email': customer.email,
                    'contact_number': customer.phone,
                    # Add any other customer details you want to include
                }}
                return Response(response_data, 200)
    
class CustomerNormalLoginView(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data

        password = data.get('password')
        username = data.get('username')
        try:
            # customer_login = CustomerNormalLogin.objects.get(username=username)
            customer_login = CustomerNormalLogin.objects.get(Q(username=username)|Q(email=username))
            # if customer_login.password is None:
            #     return Response({'is_null':True}, 404)
        except CustomerNormalLogin.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, 401)
        # customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        if check_password(password, customer_login.password):
            response_data = {'customer' : {
                'username': customer_login.username,
                'email': customer_login.email,
                'id': customer_login.customer.id,
                'name': customer_login.customer.name,
                'email': customer_login.customer.email,
                'contact_number': customer_login.customer.phone,
                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            return Response({'detail': 'Invalid credentials'}, 401)
        
class CustomerGoogleLoginView(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data

        google_id = data.get('password')
        email = data.get('email')
        try:
            # customer_login = CustomerNormalLogin.objects.get(username=username)
            customer_login = CustomerGoogleLogin.objects.get(email=email)
        except CustomerGoogleLogin.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, 401)
        # customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        if check_password(google_id, customer_login.google_id):
            response_data = {'customer' : {
                'username': customer_login.username,
                'email': customer_login.email,
                'id': customer_login.customer.id,
                'name': customer_login.customer.name,
                'email': customer_login.customer.email,
                'contact_number': customer_login.customer.phone,
                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            return Response({'detail': 'Invalid credentials'}, 401)

    

    
# class CustomerGoogleRegister(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data
#         print(data)
#         password = data.pop('password')
#         serializer = CustomerSerializer(data=data)
#         if serializer.is_valid():
#             customer = serializer.save()
#         email = data.get('email')
#         username = data.get('name')
#         customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
#         customerNormallogin.set_password(password)
#         customerNormallogin.save()
#         return Response("Customer Resistered in successfully", 200)


class CustomerGuestLoginCreate(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = request.data
        try:
            serializer = CustomerSerializer(data=posted_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
        except Exception as e:
            return Response({e}, 400)
        