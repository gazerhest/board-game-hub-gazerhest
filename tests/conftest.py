import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from games.models import Category, Publisher, BoardGame

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        username='regular_gamer',
        email='gamer@example.com',
        password='Password123!',
        is_staff=False
    )

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin_boss',
        email='admin@example.com',
        password='AdminPassword123!',
        is_staff=True
    )


@pytest.fixture
def authenticated_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def category(db):
    return Category.objects.create(
        name='Стратегія',
        slug='strategy',
        description='Ігри на стратегічне планування'
    )

@pytest.fixture
def publisher(db):
    return Publisher.objects.create(
        name='Geekach Games',
        country='Україна',
        website='https://geekach.com.ua',
    )

@pytest.fixture
def board_game(db, category, publisher):
    return BoardGame.objects.create(
        title='Catan',
        description='Освоєння острова Катан та торгівля ресурсами.',
        price=1450.00,
        min_players=3,
        max_players=4,
        play_time_minutes=75,
        min_age=10,
        release_year=2020,
        rating=8.5,
        category=category,
        publisher=publisher
    )
