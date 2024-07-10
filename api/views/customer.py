from user.models import Customer, CustomerGooglelogin, CustomerNormalLogin
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
        return Response({"data":"Customer Resgistered successfully"}, 200)
    
class CustomerGoogleRegister(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        email = data.get('email')
        username = data.get('name')
        check_email = check_email_in_normal(email) # check if email is already associated with another account
        if check_email == True:
            password = data.pop('password')
            customer = Customer.objects.get(email=email)
            customerGooglelogin = CustomerGooglelogin.objects.create(email=email, customer = customer, google_id=password)
            customerGooglelogin.set_password(password)
            customerGooglelogin.save()
            return Response({"data":"Customer Resgistered successfully"}, 200)
        else:
            password = data.pop('password')
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                customer = serializer.save()

            customerGooglelogin = CustomerGooglelogin.objects.create(email=email, customer = customer, google_id=password)
            customerGooglelogin.set_password(password)
            customerGooglelogin.save()
            return Response({"data":"Customer Resgistered successfully"}, 200)
    
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

    

    
class CustomerGoogleRegister(APIView):
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        print(data)
        password = data.pop('password')
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            customer = serializer.save()
        email = data.get('email')
        username = data.get('name')
        customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        customerNormallogin.set_password(password)
        customerNormallogin.save()
        return Response("Customer Logged in successfully", 200)


