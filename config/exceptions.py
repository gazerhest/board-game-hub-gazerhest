from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        data = {
            "status": "ERR",
            "message": "",
            "errors": None
        }
        if isinstance(response.data, dict) and "detail" in response.data:
            data["message"] = str(response.data["detail"])
        elif response.status_code == 401:
            data["message"] = "Ви не авторизовані"
        elif response.status_code == 403:
            data["message"] = "Доступ заборонено, недостатньо прав"
        elif response.status_code == 400:
            data["message"] = "Некоректні дані"
            data["errors"] = response.data
        elif response.status_code == 404:
            data["message"] = "Такого ресурсу не існує"
        else:
            data["message"] = str(exc)

        response.data = data
    return response

