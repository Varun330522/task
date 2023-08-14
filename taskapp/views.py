# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer, LoginSerializer, LoanSerializer
from django.http import JsonResponse
from .models import UserDetails, Loan
from .constants import ErrorCodes
from .checkerror import check_errors
from .utils import Loan_Approval


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
    data = {"email": email, "password": password}
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        try:
            user = UserDetails.objects.get(email=email)
        except UserDetails.DoesNotExist:
            return JsonResponse({'code': ErrorCodes.INVALID_AUTHORIZATION, 'Response_code': status.HTTP_401_UNAUTHORIZED, 'msg': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            return JsonResponse({'code': ErrorCodes.LOGIN_SUCCESSFULLY, 'Response_code': status.HTTP_202_ACCEPTED, 'msg': 'Logged in successfully'}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({'code': ErrorCodes.INCORRECT_PASSWORD, 'Response_code': status.HTTP_401_UNAUTHORIZED, 'msg': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        code_error, msg_error = check_errors(serializer.errors)
        return JsonResponse({'code': code_error, 'Response_code': status.HTTP_400_BAD_REQUEST, 'msg': msg_error}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loan_approval(request):
    user_id = request.data.get('user_id')
    amount = int(request.data.get('amount'))
    tenure = int(request.data.get('tenure'))
    salary = int(request.data.get('salary'))
    user_info = UserDetails.objects.get(id=user_id)
    if amount > salary/2:
        return JsonResponse({"code": ErrorCodes.LoanNotApproved, "status": status.HTTP_403_FORBIDDEN, "Error": "You loan will not be approved"}, status=status.HTTP_403_FORBIDDEN)
    else:
        if user_info:
            latest_loan = Loan.objects.filter(
                user_id_id=user_id, status="Active").first()
            if latest_loan:
                return JsonResponse({"code": ErrorCodes.LoanNotApproved, "status": status.HTTP_403_FORBIDDEN, "error": "You already has loan you can't apply"}, status=status.HTTP_403_FORBIDDEN)
            else:
                interest, processing_fee = Loan_Approval.calculate_int_processing_fee(
                    amount, tenure)
                loan_id = Loan.generate_loanId()
                data = {"loan_id": loan_id, "amount": amount, "tenure_month": tenure,
                        "user_id": user_info.id, "status": 'Active'}
                serializer = LoanSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {"disbersal_amount": amount -
                                     processing_fee, "total_payable": amount+interest, "interest": interest, "tenure": tenure, "processing_fee": processing_fee}
                    return JsonResponse({"code": ErrorCodes.LoanApproved, "status": status.HTTP_202_ACCEPTED, "msg": "Loan Approved", "data": response_data}, status=status.HTTP_202_ACCEPTED)
                else:
                    error = []
                    for key, value in serializer.errors.items():
                        error_dict = dict()
                        error_dict['field'] = key
                        if 'code' in value:
                            error_dict['code'] = value.get('code')
                            error_dict['message'] = value.get('message')
                        else:
                            error_dict['message'] = value[0]
                            error.append(error_dict)
                    return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"code": ErrorCodes.UserNotApproved, "status": status.HTTP_404_NOT_FOUND, "error": "Invalid User"}, status=status.HTTP_404_NOT_FOUND)
