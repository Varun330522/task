# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from django.http import JsonResponse
from .models import UserDetails
from .constants import ErrorCodes
from .checkerror import check_errors


@api_view(['POST'])
def register_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username:
            return JsonResponse({"code": ErrorCodes.MISSING_USERNAME, "ResponseCode": status.HTTP_400_BAD_REQUEST, "message": "Username is required", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return JsonResponse({"code": ErrorCodes.MISSING_EMAIL, "ResponseCode": status.HTTP_400_BAD_REQUEST, "message": "Email is required", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return JsonResponse({"code": ErrorCodes.MISSING_PASSWORD, "ResponseCode": status.HTTP_400_BAD_REQUEST, "message": "Password is required", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        data = {"username": username, "password": password, "email": email}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            dataTosend = {
                'email': serializer.validated_data.get('email'),
                'username': serializer.validated_data.get('username'),
                'user_id': serializer.data.get('id')
            }
            return JsonResponse({"code": ErrorCodes.Success, "ResponseCode": status.HTTP_201_CREATED, "message": "User registered successfully", "data": dataTosend}, status=status.HTTP_201_CREATED)
        else:
            code_error, msg_error = check_errors(serializer.errors)
            return JsonResponse({"code": code_error, "ResponseCode": status.HTTP_406_NOT_ACCEPTABLE, "message": msg_error, "data": {}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    try:
        user = UserDetails.objects.get(email=email)
    except UserDetails.DoesNotExist:
        return JsonResponse({'msg': "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if check_password(password, user.password):
        return JsonResponse({'msg': 'Logged in successfully'}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'msg': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
