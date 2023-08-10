from .constants import ErrorCodes, ErrorMessage


def check_errors(validate_error):
    code_error = []
    msg_error = []
    for key, value in validate_error.items():
        if key == 'username':
            code, msg = check_username(value[0])
            code_error.append(code)
            msg_error.append(msg)
        if key == 'email':
            code, msg = check_email(value[0])
            code_error.append(code)
            msg_error.append(msg)
        if key == 'password':
            code, msg = check_password(value[0])
            code_error.append(code)
            msg_error.append(msg)
    return code_error, msg_error


def check_username(username_error):
    if ErrorMessage.USERNAME_EXIST == username_error:
        return ErrorCodes.USERNAME_EXIST, ErrorMessage.USERNAME_EXIST
    if ErrorMessage.USERNAME_WORDS == username_error:
        return ErrorCodes.USERNAME_WORDS, ErrorMessage.USERNAME_WORDS


def check_password(password_error):
    if ErrorMessage.INVALID_PASSWORD == password_error:
        return ErrorCodes.INVALID_PASSWORD, ErrorMessage.INVALID_PASSWORD
    if ErrorMessage.PASSWORD_LENGTH == password_error:
        return ErrorCodes.PASSWORD_LENGTH, ErrorMessage.PASSWORD_LENGTH


def check_email(email_error):
    if ErrorMessage.EMAIL_EXIST == email_error:
        return ErrorCodes.EMAIL_EXIST, ErrorMessage.EMAIL_EXIST
    if ErrorMessage.INVALID_EMAIL == email_error:
        return ErrorCodes.EMAILINVALID_ERROR, ErrorMessage.INVALID_EMAIL
