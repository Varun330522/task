from .constants import ErrorCodes, ErrorMessage

ERROR_MAPPING = {
    'username': {
        ErrorMessage.USERNAME_EXIST: ErrorCodes.USERNAME_EXIST,
        ErrorMessage.USERNAME_WORDS: ErrorCodes.USERNAME_WORDS
    },
    'email': {
        ErrorMessage.EMAIL_EXIST: ErrorCodes.EMAIL_EXIST,
        ErrorMessage.INVALID_EMAIL: ErrorCodes.EMAILINVALID_ERROR
    },
    'password': {
        ErrorMessage.INVALID_PASSWORD: ErrorCodes.INVALID_PASSWORD,
        ErrorMessage.PASSWORD_LENGTH: ErrorCodes.PASSWORD_LENGTH
    },
}


def check_errors(validate_error):
    code_error = []
    msg_error = []
    for key, value in validate_error.items():
        code, msg = check_field(key, value[0])
        code_error.append(code)
        msg_error.append(msg)
    return code_error, msg_error


def check_field(field, field_error):
    if field in ERROR_MAPPING and field_error in ERROR_MAPPING[field]:
        return ERROR_MAPPING[field][field_error], field_error
    return ErrorCodes.UNKNOWN_ERROR, ErrorMessage.UNKNOWN_ERROR
