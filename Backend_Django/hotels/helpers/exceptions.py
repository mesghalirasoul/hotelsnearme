from rest_framework.exceptions import APIException

class HTTP_400_BAD_REQUEST(APIException):
    status_code = 400
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'