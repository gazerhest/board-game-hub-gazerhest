import pytest
from rest_framework import status
from games.models import BoardGame


@pytest.mark.django_db
class TestBoardGameHappy:
    def test_get_games_list_anonymous(self, api_client, board_game):
        response = api_client.get("/api/v1/games/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == board_game.title
        assert response.data[0]['price'] == '1450.00'

    def test_get_game_detail(self, api_client, board_game):
        response = api_client.get(f"/api/v1/games/{board_game.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == board_game.id
        assert response.data['title'] == 'Catan'
        assert response.data['category']['name'] == 'Стратегія'
        assert response.data['publisher']['name'] == 'Geekach Games'

    def test_search_game_by_title(self, api_client, board_game, category, publisher):
        BoardGame.objects.create(
            title='Каркасон',
            description='Середньовічні замки та дороги.',
            price=950.00,
            min_players=2,
            max_players=5,
            play_time_minutes=45,
            min_age=8,
            release_year=2000,
            category=category,
            publisher=publisher
        )
        response = api_client.get("/api/v1/games/?search=Catan")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Catan'

    def test_create_game_as_admin(self, admin_client, category, publisher):
        data_json = {
            "title": "Дюна: Імперіум",
            "description": "Боротьба за владу на пустельній планеті Арракіс.",
            "price": 2100.00,
            "min_players": 1,
            "max_players": 4,
            "play_time_minutes": 120,
            "min_age": 14,
            "release_year": 2020,
            "category_id": category.id,
            "publisher_id": publisher.id
        }
        response = admin_client.post("/api/v1/games/", data_json)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == "Дюна: Імперіум"
        assert BoardGame.objects.filter(title="Дюна: Імперіум").exists()

    def test_partial_update_game_as_admin(self, admin_client, board_game):
        url = f"/api/v1/games/{board_game.id}/"
        response = admin_client.patch(url, data={"price":1699.00})
        assert response.status_code == status.HTTP_200_OK
        board_game.refresh_from_db()
        assert float(board_game.price) == 1699.00

    def test_delete_game_as_admin(self, admin_client, board_game):
        response = admin_client.delete(f"/api/v1/games/{board_game.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BoardGame.objects.filter(id=board_game.id).exists()


@pytest.mark.django_db
class TestBoardGameSad:
    def test_create_game_unauthorized(self, api_client, category, publisher):
        data_json = {
            "title": "Хижа гра",
            "description": "Спроба зламу.",
            "price": 1000.00,
            "min_players": 2,
            "max_players": 4,
            "play_time_minutes": 60,
            "min_age": 10,
            "release_year": 2024,
            "category_id": category.id,
            "publisher_id": publisher.id
        }
        response = api_client.post("/api/v1/games/", data_json)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['status'] == 'ERR'
        assert "Ви не авторизовані" in response.data['message']
        assert not BoardGame.objects.filter(title="Хижа гра").exists()

    def test_create_game_forbidden(self, authenticated_client, category, publisher):
        data_json = {
            "title": "Звичайна гра",
            "description": "Спроба звичайного юзера.",
            "price": 500.00,
            "min_players": 2,
            "max_players": 4,
            "play_time_minutes": 30,
            "min_age": 8,
            "release_year": 2024,
            "category_id": category.id,
            "publisher_id": publisher.id
        }
        response = authenticated_client.post("/api/v1/games/", data_json)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['status'] == 'ERR'
        assert "Доступ заборонено, недостатньо прав" in response.data['message']
        assert not BoardGame.objects.filter(title="Звичайна гра").exists()

    def test_delete_game_forbidden(self, authenticated_client, board_game):
        response = authenticated_client.delete(f"/api/v1/games/{board_game.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BoardGame.objects.filter(id=board_game.id).exists()

    def test_create_game_invalid_1(self, admin_client, category, publisher):
        data_json = {
            "title": "Безкоштовна гра",
            "description": "Тест від'ємної ціни.",
            "price": -150.00,
            "min_players": 2,
            "max_players": 4,
            "play_time_minutes": 60,
            "min_age": 10,
            "release_year": 2024,
            "category_id": category.id,
            "publisher_id": publisher.id
        }
        response = admin_client.post("/api/v1/games/", data_json)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'ERR'
        assert 'price' in response.data['errors']

    def test_create_game_invalid_2(self, admin_client, category, publisher):
        data_json = {
            "title": "Безкоштовна гра",
            "description": "Тест від'ємної ціни.",
            "price": 150.00,
            "min_players": 6,
            "max_players": 4,
            "play_time_minutes": 60,
            "min_age": 10,
            "release_year": 2024,
            "category_id": category.id,
            "publisher_id": publisher.id
        }
        response = admin_client.post("/api/v1/games/", data_json)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'ERR'
        assert 'min_players' in response.data['errors']

    def test_not_found(self, api_client):
        response = api_client.get("/api/v1/games/6767/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'ERR'
        assert "не знайдено" in response.data['message']

    def test_delete_not_found(self, admin_client):
        response = admin_client.delete("/api/v1/games/676767/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'ERR'
