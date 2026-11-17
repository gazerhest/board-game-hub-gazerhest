from django.db.models import Q, ProtectedError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Publisher, Designer, BoardGame
from .serializers import (
    CategorySerializer,
    PublisherSerializer,
    PublisherDetailSerializer,
    DesignerSerializer,
    DesignerDetailSerializer,
    BoardGameSerializer
)
from .permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import ErrorResponseSerializer
import logging
logger = logging.getLogger(__name__)

def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": "ERR",
        "message": message,
        "errors": errors
    }, status=status_code)


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response("Некоректні дані для створення категорії", serializer.errors)


class CategoryDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None
    
    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response(f"Категорію з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response(f"Категорію з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення категорії", serializer.errors)

    def patch(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response(f"Категорію з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення категорії", serializer.errors)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response(f"Категорію з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        try:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            logger.warning(f"ProtectedError: failed delete category (id={pk}) by admin {request.user.username}")
            return error_response(
                "Неможливо видалити категорію, оскільки до неї прив'язані настільні ігри",
                status_code=status.HTTP_400_BAD_REQUEST
            )


class PublisherListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response("Некоректні дані для створення видавництва", serializer.errors)


class PublisherDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Publisher.objects.prefetch_related('games').get(pk=pk)
        except Publisher.DoesNotExist:
            return None

    def get(self, request, pk):
        publisher = self.get_object(pk)
        if not publisher:
            return error_response(f"Видавництва з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = PublisherDetailSerializer(publisher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        publisher = self.get_object(pk)
        if not publisher:
            return error_response(f"Видавництво з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення видавництва", serializer.errors)

    def patch(self, request, pk):
        publisher = self.get_object(pk)
        if not publisher:
            return error_response(f"Видавництво з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = PublisherSerializer(publisher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення видавництва", serializer.errors)

    def delete(self, request, pk):
        publisher = self.get_object(pk)
        if not publisher:
            return error_response(f"Видавництво з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        try:
            publisher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            logger.warning(f"ProtectedError: failed delete publisher (id={pk}) by admin {request.user.username}")
            return error_response(
                "Неможливо видалити видавництво, оскільки до нього прив'язані якісь настільні ігри", status_code=status.HTTP_400_BAD_REQUEST
            )
        
class DesignerListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        designers = Designer.objects.all()
        serializer = DesignerSerializer(designers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DesignerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response("Некоректні дані для додавання автора", serializer.errors)


class DesignerDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Designer.objects.prefetch_related('games').get(pk=pk)
        except Designer.DoesNotExist:
            return None

    def get(self, request, pk):
        designer = self.get_object(pk)
        if not designer:
            return error_response(f"Автора з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = DesignerDetailSerializer(designer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        designer = self.get_object(pk)
        if not designer:
            return error_response(f"Автора з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = DesignerSerializer(designer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення автора", serializer.errors)

    def patch(self, request, pk):
        designer = self.get_object(pk)
        if not designer:
            return error_response(f"Автора з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = DesignerSerializer(designer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для оновлення автора", serializer.errors)

    def delete(self, request, pk):
        designer = self.get_object(pk)
        if not designer:
            return error_response(f"Автора з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        designer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardGameListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Отримати список ігор",
        auth=[],
        parameters=[
            OpenApiParameter(name='search', description='пошук', required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='category', description='id категорії для фільтру', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='publisher', description='id публішера для фільтру', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='designer', description='id автора для фільтру', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='min_players', description='ігри, які підходять під таку компанію', required=False,
                             type=OpenApiTypes.INT),
            OpenApiParameter(name='ordering', description='сортування за', required=False, type=OpenApiTypes.STR,
                             enum=['price', '-price', 'rating', '-rating', 'title', '-created_at'])
        ],
        responses={200: BoardGameSerializer(many=True)}
    )
    def get(self, request):
        queryset = BoardGame.objects.select_related('category', 'publisher', 'designer').all()

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        publisher_id = request.query_params.get('publisher')
        if publisher_id:
            queryset = queryset.filter(publisher_id=publisher_id)

        designer_id = request.query_params.get('designer')
        if designer_id:
            queryset = queryset.filter(designer_id=designer_id)

        min_players = request.query_params.get('min_players')
        if min_players:
            queryset = queryset.filter(min_players__lte=min_players, max_players__gte=min_players)

        ordering = request.query_params.get('ordering')
        allowed_ordering = ['price', '-price', 'rating', '-rating', 'title', '-created_at']
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        serializer = BoardGameSerializer(queryset, many=True)
        logger.debug(f"query for games list, param: {dict(request.query_params)}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Створити нову гру (доступно тільки адміну)",
        request=BoardGameSerializer,
        responses={
            201: BoardGameSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
            403: ErrorResponseSerializer
        },
        examples=[
            OpenApiExample(
                'Приклад створення',
                value={
                    "title": "Дюна: Імперіум",
                    "description": "Колодобудівна стратегія за мотивами всесвіту Дюни.",
                    "price": "2100.00",
                    "min_players": 1,
                    "max_players": 4,
                    "play_time_minutes": 120,
                    "min_age": 14,
                    "release_year": 2020,
                    "rating": "9.1",
                    "category_id": 1,
                    "publisher_id": 1
                },
                request_only=True
            ),
            OpenApiExample(
                'BAD REQUEST 400',
                value={
                    "status": "ERR",
                    "message": "Некоректні дані для створення гри",
                    "errors": {"price": ["Ціна гри повинна бути більшою за нуль"]}
                },
                response_only=True,
                status_codes=['400']
            )
        ]
    )
    def post(self, request):
        serializer = BoardGameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            output_serializer = BoardGameSerializer(game)
            logger.info(f"admin '{request.user.username}' created game '{game.title}', game id={game.id}")
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"validation error while creating a game; user - {request.user.username}, {serializer.errors}")
        return error_response("Некоректні дані для створення гри", serializer.errors)


class BoardGameDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return BoardGame.objects.select_related('category', 'publisher', 'designer').get(pk=pk)
        except BoardGame.DoesNotExist:
            return None

    @extend_schema(
        summary="отримати інформацію про одну гру",
        auth=[],
        responses={
            200: BoardGameSerializer,
            404: ErrorResponseSerializer
        }
    )
    def get(self, request, pk):
        game = self.get_object(pk)
        if not game:
            logger.warning(f"query for non-existing game ID={pk}; method={request.method}")
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game)
        logger.debug(f"query for game, id={pk}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="оновити гру (повністю)",
        request=BoardGameSerializer,
        responses={
            200: BoardGameSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        }
    )
    def put(self, request, pk):
        game = self.get_object(pk)
        if not game:
            logger.warning(f"query for non-existing game ID={pk}; method={request.method}")
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game, data=request.data)
        if serializer.is_valid():
            updated_game = serializer.save()
            logger.info(f"admin '{request.user.username}' updated game; id={pk}")
            return Response(BoardGameSerializer(updated_game).data, status=status.HTTP_200_OK)
        logger.warning(f"failed update game (va_err) by admin '{request.user.username}'; id={pk}; method={request.method}")
        return error_response("Некоректні дані для повного оновлення гри", serializer.errors)

    @extend_schema(
        summary="оновити гру (частково)",
        request=BoardGameSerializer,
        responses={
            200: BoardGameSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer
        }
    )
    def patch(self, request, pk):
        game = self.get_object(pk)
        if not game:
            logger.warning(f"query for non-existing game ID={pk}; method={request.method}")
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            updated_game = serializer.save()
            logger.info(f"admin '{request.user.username}' updated game; id={pk}")
            return Response(BoardGameSerializer(updated_game).data, status=status.HTTP_200_OK)
        logger.warning(f"failed update game (va_err) by admin '{request.user.username}'; id={pk}; method={request.method}")
        return error_response("Некоректні дані для часткового оновлення гри", serializer.errors)

    @extend_schema(
        summary="видалити гру",
        responses={
            204: BoardGameSerializer,
            401: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer
        }
    )
    def delete(self, request, pk):
        game = self.get_object(pk)
        if not game:
            logger.warning(f"query for non-existing game ID={pk}; method={request.method}")
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        game.delete()
        logger.info(f"admin '{request.user.username}' deleted game; id={pk}")
        return Response(status=status.HTTP_204_NO_CONTENT)


