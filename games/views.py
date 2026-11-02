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


def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors
    }, status=status_code)


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all();
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response("Некоректні дані для створення категорії", serializer.errors)


class CategoryDetailAPIView(APIView):
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
            return error_response(
                "Неможливо видалити категорію, оскільки до неї прив'язані настільні ігри",
                status_code=status.HTTP_400_BAD_REQUEST
            )


class PublisherListCreateAPIView(APIView):
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
            return error_response(
                "Неможливо видалити видавництво, оскільки до нього прив'язані якісь настільні ігри", status_code=status.HTTP_400_BAD_REQUEST
            )
        
class DesignerListCreateAPIView(APIView):
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardGameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            output_serializer = BoardGameSerializer(game)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return error_response("Некоректні дані для створення гри", serializer.errors)


class BoardGameDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return BoardGame.objects.select_related('category', 'publisher', 'designer').get(pk=pk)
        except BoardGame.DoesNotExist:
            return None

    def get(self, request, pk):
        game = self.get_object(pk)
        if not game:
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        game = self.get_object(pk)
        if not game:
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game, data=request.data)
        if serializer.is_valid():
            updated_game = serializer.save()
            return Response(BoardGameSerializer(updated_game).data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для повного оновлення гри", serializer.errors)

    def patch(self, request, pk):
        game = self.get_object(pk)
        if not game:
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = BoardGameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            updated_game = serializer.save()
            return Response(BoardGameSerializer(updated_game).data, status=status.HTTP_200_OK)
        return error_response("Некоректні дані для часткового оновлення гри", serializer.errors)

    def delete(self, request, pk):
        game = self.get_object(pk)
        if not game:
            return error_response(f"Гру з ID {pk} не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


