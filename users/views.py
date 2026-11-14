from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "Ви успішно зареєстровані.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Виникла помилка при валідації реєстрування",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({
                "status": "error",
                "message": "Для logout потрібно надати рефрещ-токен",
                "errors": {"refresh": ["Поле 'refresh' є обов'язковим"]}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": "success",
                "message": "Ви успішно лог-аутнулись"
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                "status": "error",
                "message": "недійсний/кривий токен",
                "errors": str(TokenError)
            }, status=status.HTTP_400_BAD_REQUEST)








