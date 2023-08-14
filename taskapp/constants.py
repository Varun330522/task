class ErrorCodes:
    Success = 10000
    EMAILINVALID_ERROR = 10001
    EMAIL_EXIST = 10002
    MISSING_EMAIL = 10003
    PASSWORD_LENGTH = 10004
    INVALID_PASSWORD = 10005
    MISSING_PASSWORD = 10006
    USERNAME_EXIST = 10007
    USERNAME_WORDS = 10008
    MISSING_USERNAME = 10009
    INVALID_AUTHORIZATION = 10010
    LOGIN_SUCCESSFULLY = 10011
    INVALID_LOGINPASSWORD = 10012
    INCORRECT_PASSWORD = 10013
    LoanApproved = 10014
    LoanNotApproved = 10015
    UserNotApproved = 10016


class ErrorMessage:
    USERNAME_EXIST = "user with this username already exists."
    USERNAME_WORDS = "Ensure this field has no more than 150 characters."
    EMAIL_EXIST = "user with this email already exists."
    INVALID_EMAIL = "Enter a valid email address."
    PASSWORD_LENGTH = "Password must be at least 8 characters long."
    INVALID_PASSWORD = "Password must meet the complexity requirements."


class CONSTANTS:
    INTEREST = 35.88
    YEAR = 12
