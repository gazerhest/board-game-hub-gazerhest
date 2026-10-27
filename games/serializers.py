from datetime import date
from rest_framework import serializers
from .models import Category, Publisher, Designer, BoardGame


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'website', 'description']


class DesignerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Designer
        fields = ['id', 'first_name', 'last_name', 'full_name', 'bio']


class BoardGameShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGame
        fields = ['id', 'title', 'price', 'rating']


class PublisherDetailSerializer(serializers.ModelSerializer):
    games = BoardGameShortSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'website', 'description', 'games']


class DesignerDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    games = BoardGameShortSerializer(many=True, read_only=True)

    class Meta:
        model = Designer
        fields = ['id', 'first_name', 'last_name', 'full_name', 'bio', 'games']


class BoardGameSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    designer = DesignerSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(), source='publisher', write_only=True
    )
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), source='designer', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = BoardGame
        fields = [
            'id', 'title', 'description', 'price',
            'min_players', 'max_players', 'play_time_minutes',
            'min_age', 'release_year', 'rating', 'image_url',
            'category', 'publisher', 'designer',
            'category_id', 'publisher_id', 'designer_id',
            'created_at', 'updated_at'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ціна гри повинна бути більшою за нуль")
        return value

    def validate_play_time_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError("Тривалість партії має бути додатною")
        return value

    def validate_min_players(self, value):
        if value < 1:
            raise serializers.ValidationError("Мінімальна кількість гравців має бути щонайменше 1")
        return value

    def validate_release_year(self, value):
        max_year = date.today().year + 1
        if value < 1900 or value > max_year:
            raise serializers.ValidationError(f"Рік випуску має бути в межах від 1900 до {max_year}")
        return value

    def validate_rating(self, value):
        if value < 0.0 or value > 10.0:
            raise serializers.ValidationError("Рейтинг повинен бути в межах від 0.0 до 10.0")
        return value

    def validate(self, attrs):
        min_p = attrs.get('min_players', getattr(self.instance, 'min_players', None))
        max_p = attrs.get('max_players', getattr(self.instance, 'max_players', None))

        if min_p is not None and max_p is not None and min_p > max_p:
            raise serializers.ValidationError({
                "min_players": "Мінімальна кількість гравців не може бути більшою за максимальну"
            })
        return attrs
    