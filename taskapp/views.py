# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from django.http import JsonResponse
from .models import UserDetails


@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            return JsonResponse({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
