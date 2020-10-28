from rest_framework import renderers
from rest_framework.views import exception_handler
import re

class CustomJSONRenderer(renderers.JSONRenderer):

    def render(self, data ,accepted_media_type=None, renderer_context=None):
        if(data is not None and isinstance(data,list)):
            response_data = { 'message': data[1],'status': 'success', 'data': data[0]}
        else:
            errors = []
            message = data.get('detail')
            if not message:
               for field, value in data.items():    
                   errors.append("{} : {}".format(field, " ".join(value)))
               response_data = {'data': [], 'message': 'Validation Error', 'errors': errors, 'status': 'failure','data': []}
            else:
                errors = get_codes(message)
                response_data = {'message': message, 'errors': errors, 'status': 'failure','data': []}  
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        return response

def get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: get_codes(value) for key, value in detail.items()}
    return detail.code