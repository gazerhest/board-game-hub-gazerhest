from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    view = context.get('view')

    view_name = view.__class__.__name__ if view else "?view?"
    method = request.method if request else "?method?"
    path = request.path if request else "?path?"

    if request and hasattr(request, 'user') and request.user and request.user.is_authenticated:
        user_info = request.user.username
    else:
        user_info = "anonymous"

    if response is not None:
        data = {
            "status": "ERR",
            "message": "",
            "errors": None
        }
        if response.status_code == 401:
            data["message"] = "Ви не авторизовані"
        elif response.status_code == 403:
            data["message"] = "Доступ заборонено, недостатньо прав"
        elif response.status_code == 404:
            data["message"] = "Такого ресурсу не існує"
        elif response.status_code == 400:
            if isinstance(response.data, dict) and "detail" in response.data:
                data["message"] = str(response.data["detail"])
            else:
                data["message"] = "Некоректні дані"
                data["errors"] = response.data
        elif isinstance(response.data, dict) and "detail" in response.data:
            data["message"] = str(response.data["detail"])
        else:
            data["message"] = str(exc)

        logger.warning(f"http {response.status_code} || {method} {path} || view - {view_name} || user - {user_info} || reason-  {data['message']}")

        response.data = data
    else:
        logger.error(f"ERR on server (500) || {method} {path} || view - {view_name} || user - {user_info}", exc_info=True)

    return response

