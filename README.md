# board-game hub - платформа на базі Django REST Framework для інтернет-магазину/ком'юніті настільних ігор. 

## Основний функціонал
+ Каталог настільних ігор - перегляд ігор із пошуком за назвою, фільтрацією за видавництвами, дизайнерами, жанрами/механіками, кількістю гравців, віковими обмеженнями та сортуванням (за ціною, популярністю, рейтингом) і т.д.
+ Картки видавництв та авторів - можливість перегляду каталогу ігор, згрупованих за конкретним українським чи міжнародним видавництвом або автором гри.
+ Кошик і замовлення - якщо юзер авторизований, він може додавати товари до кошика, змінювати к-сть та робити замовлення з фіксацією ціни на момент покупки.
+ Адміністративне управління CRUD - create/read/update/delete цих ігор та видавництв і т.д.
+ Загальна інформація - сторінка контактів, правил на доставку, повернення товару.
+ Автентифікація через JWT-токен

---

## How to run project

1. Create virtual env
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Copy instance-file into your own `.env`:
```bash
cp .env.example .env
```
4. Create and apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Run the server
```bash
python manage.py runserver
```

---

## Tests/coverage
Запуск тестів:
```bash
pytest -v
```

coverage:
```bash
coverage run -m pytest
coverage report -m
```

результат:
```bash
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
config\__init__.py                     0      0   100%
config\exceptions.py                  22     10    55%   16-27
config\settings.py                    26      0   100%
config\urls.py                         3      0   100%
games\__init__.py                      0      0   100%
games\admin.py                         1      0   100%
games\apps.py                          3      0   100%
games\migrations\0001_initial.py       6      0   100%
games\migrations\__init__.py           0      0   100%
games\models.py                       49      5    90%   12, 25, 38, 41, 81
games\permissions.py                   6      0   100%
games\serializers.py                  68      6    91%   82, 87, 93, 97-99
games\tests.py                         1      0   100%
games\urls.py                          3      0   100%
games\views.py                       231    135    42%   27-29, 32-36, 42-45, 48-52, 55-62, 65-72, 75-82, 91-93, 96-100, 106-109, 112-116, 119-126, 129-136, 139-146, 153-155, 158-162, 168-171, 174-178, 181-188, 191-198, 201-205, 219, 223, 227, 231, 236, 266-273, 278, 283
tests\conftest.py                     30      0   100%
tests\test_games.py                   81      0   100%
users\__init__.py                      0      0   100%
users\admin.py                         1      0   100%
users\apps.py                          3      0   100%
users\migrations\__init__.py           0      0   100%
users\models.py                        1      0   100%
users\serializers.py                  32     12    62%   63-65, 68-70, 73-75, 78-86
users\tests.py                         1      0   100%
users\urls.py                          4      0   100%
users\views.py                        27     14    48%   14-22, 32-49
----------------------------------------------------------------
TOTAL                                599    182    70%
```

---

## API documentation
бібліотека - `drf-spectacular`
після запуску сервера, до документації можна дістатись по адресі:
```bash
http://127.0.0.1:8000/swagger/
```

генерація OPenAPI-схеми:
```bash
http://127.0.0.1:8000/api/scheme/
```
або ж натиснути на кнопку `api/scheme` на сторінці документації на Swagger.

---

## DB schema
+ `users` - користувачі (id, username, email, first_name, last_name, is_staff, created_at).
+ `categories` - жанри/механіки ігор (id, name, slug, description).
+ `publishers` - публішери (id, name, country, website, description).
+  `designers` - автори/дизайнери ігор (id, full_name, bio).
+ `board_games` - основний каталог настільних ігор:
   * `id` (PK);
   * `title` (VARCHAR);
   * `description` (TEXT);
   * `price` (DECIMAL);
   * `min_players`, `max_players` (INT);
   * `play_time_minutes` (INT);
   * `min_age` (INT);
   * `release_year` (INT);
   * `rating` (DECIMAL);
   * `image_url` (VARCHAR);
   * `publisher_id` (FK до `publishers`);
   * `category_id` (FK до `categories`);
   * `designer_id` (FK до `designers`);
6. `carts` - кошик юзера (`id`, `user_id` [FK]).
7. `cart_items` - товари кошику (`id`, `cart_id` [FK], `game_id` [FK], `quantity`).
8. `orders` - замовлення (`id`, `user_id` [FK], `created_at`, `status`, `total_price`).
9. `order_items`- фіксовані позиції замовлення (`id`, `order_id` [FK], `game_id` [FK], `quantity`, `unit_price`).
10. `store_info` - інфо про магазин (`id`, `about_us`, `delivery_info`, `return_policy`, `phone`, `email`, `address`).

---

## Доступ до закритих ендпоінтів
Для доступу до них клієнт має надати (перед цим отриманий) access токен в кожному запиті в заголовку Authorization:
`Authorization: Bearer <example_access_t>`

## Ролі та доступ
Щодо каталогу - всім (і неавторизованим тоже) користувачам доступний метод GET щодо всіх головних ендпоінтів, зв'язаних з тематикою ігор
всі решта методів - для ролі адміністраторів (GET звісно також дозволяється)

# Помилки доступу
Якщо користувач неавторизований (себто не має токена, ні access, ні refresh), повертається 401-Код
Якщо запит надісланий ЗАЛОГІНЕНИМ користувачем методами, які дозволені лише адміністраторам, викидається з 403-кодом

## Ендпоінти
# Ендпоінти authN
* реєстрація
  * Метод: `POST`
  * URL: `/api/v1/auth/register/`
  * Доступ: public
  * request body JSON:
  ```json
  {
    "username": "boardgamer",
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "password_confirmation": "SecurePassword123!",
    "first_name": "Тарас",
    "last_name": "Шевченко"
  }
  ```
  * Валідація: умови дотримано
  * SUCCESS 201:
  ```JSON
  {
    "status": "success",
    "message": "Ви успішно зареєстровані.",
    "user": {
      "id": 2,
      "username": "boardgamer",
      "email": "user@example.com",
      "first_name": "Тарас",
      "last_name": "Шевченко",
      "is_staff": false
    }
  }
  ```
  * FAILURE 400:
  ```JSON
  {
    "status": "error",
    "message": "Виникла помилка при валідації реєстрування",
    "errors": {
      "password_confirmation": ["Паролі не співпадають"],
      "email": ["Некоректна електронна пошта"]
    }
  }
  ```

* Login (refresh/access):
  * Метод: `POST`
  * URL: `/api/v1/auth/login/`
  * Доступ: public
  * request body JSON:
  ```JSON
  {
    "username": "boardgamer",
    "password": "SecurePassword123!"
  }
  ```
  * SUCCESS 200:
  ```JSON
  {
    "access": "abcdeABCDE...",
    "refresh": "ABCDEabcde..."
  }
  ```
  * FAILURE 401:
  ```JSON
  {
    "status": "error",
    "message": "No active account found with the given credentials",
    "errors": null
  }
  ```

* access через refresh токен
  * Метод: `POST`
  * URL: `/api/v1/auth/refresh/`
  * Доступ: public
  * request body JSON:
  ```JSON
  {
    "refresh": "abcdeandf..."
  }
  ```
  * SUCCESS 200:
  ```JSON
  {
    "access": "dsfsdfsd..."
  }
  ```

* logout
  * Метод: `POST`
  * URL: `/api/v1/auth/logout/`
  * Доступ: [IsAuthenticated]
  * request body JSON:
  ```JSON
  {
    "refresh": "khksdbfkjsdn..."
  }
  ```
  * SUCCESS 200:
  ```JSON
  {
    "status": "success",
    "message": "Ви успішно лог-аутнулись"
  }
  ```

Настільні ігри (каталог) `/games`:
* список ігор
  * Метод: `GET`
  * URL: `/api/v1/games/`
  * Query-параметри
    * `search` (стрінга) - (`?search=Catan`)
    * `category` (int) - (`?category=2`)
    * `publisher` (int) - (`?publisher=1`)
    * `designer` (int) - (`?designer=3`)
    * `min_players` (int) - (`?min_players=2`)
    * `ordering` (стрінга) - сортування: `price` (від дешевих), `-price` (від дорогих), `-rating` (за популярністю), `title`
    * `page` (int) - для пагінації
  * Response Status: `200 OK`

* отримати детальну інформацію про гру
  * Метод: '`GET`
  * URL: `/api/v1/games/{id}/`
  * Response Status: `200 OK` (або `404` Not Found)
  * Response Body (JSON):
```json
{
  "id": 1,
  "title": "Catan: Колонізатори",
  "description": "Класична економічна стратегія про освоєння острова Катан. Гравці добувають ресурси, торгують та будують поселення.",
  "price": "1450.00",
  "min_players": 3,
  "max_players": 4,
  "play_time_minutes": 75,
  "min_age": 10,
  "release_year": 1995,
  "rating": 4.8,
  "image_url": "https://example.com/catan.jpg",
  "category": { "id": 1, "name": "Стратегія" },
  "publisher": { "id": 1, "name": "Geekach Games" },
  "designer": { "id": 1, "full_name": "Klaus Teuber" }
}
```

* [admin] створити гру
  * Метод: `POST`
  * URL: `/api/v1/games/`
  * Response Status: `201 Created` або ' (або 400 Bad Request, 401 Unauthorized)'
  * Request Body (JSON):
```json
{
  "title": "Dune: Імперіум",
  "description": "Колодобудівна стратегія за мотивами всесвіту Дюни.",
  "price": "2100.00",
  "min_players": 1,
  "max_players": 4,
  "play_time_minutes": 120,
  "min_age": 14,
  "release_year": 2020,
  "image_url": "https://example.com/dune.jpg",
  "category_id": 1,
  "publisher_id": 2,
  "designer_id": 4
}
```

* [admin] оновити гру
  * Метод: `PUT`/`PATHC`
  * URL: `/api/v1/games/{id}/`
  * Response Status: `200 OK`

* [admin] видалити гру
  * Метод: `DELETE`
  * URL: `/api/v1/games/{id}/`
  * Response Status: `204 No Content`


ВИДАВНИЦТВА (`/publishers`)
* отрмати список видавництв
  * Метод: `GET`
  * URL: `/api/v1/publishers/`
  * Response Status: `200 OK`
  * Response Body (JSON):
```json
[
  {
    "id": 1,
    "name": "Geekach Games",
    "country": "Україна",
    "website": "https://geekach.com.ua"
  }
]
```

* сторінка видавництва
  * Метод: `GET`
  * URL: `/api/v1/publishers/{id}`
  * Response Status: `200 OK`
  * Response Body (JSON):
```json
{
  "id": 1,
  "name": "Geekach Games",
  "country": "Україна",
  "website": "https://geekach.com.ua",
  "description": "Українське локалізаційне видавництво настільних ігор.",
  "games": [
    {
      "id": 1,
      "title": "Catan: Колонізатори",
      "price": "1450.00",
      "rating": 4.8
    }
  ]
}
```
* [admin] create/put/delete видавництво
  * Методи: `POST /publishers/`, `PUT /publishers/{id}/`, `DELETE /publishers/{id}/`
 
ДИЗАЙНЕРИ ІГОР (`/designers`)
* отрмати список дизайнерів
  * Метод: `GET`
  * URL: `/api/v1/designers/`
  * Response Status: `200 OK`

* сторінка автора, всі його ігри
  * Метод: `GET`
  * URL: `/api/v1/designers/{id}`
  * Response Status: `200 OK`
  * Response Body (JSON):
```json
{
  "id": 1,
  "full_name": "Klaus Teuber",
  "bio": "Німецький геймдизайнер, творець легендарної серії Catan.",
  "games": [
    {
      "id": 1,
      "title": "Catan: Колонізатори",
      "price": "1450.00"
    }
  ]
}
```

КАТЕГОРІЇ ТА ЖАНРИ (`/categories`)
  * отримати список категорій
    * Метод: `GET`
    * URL: `/api/v1/categories/`
    * Response Status: `200 OK`
    * Response Body (JSON):
```json
[
  { "id": 1, "name": "Стратегії", "slug": "strategy" },
  { "id": 2, "name": "Для вечірок (Party Games)", "slug": "party" }
]
```

АУНТЕФІКАЦЯ ТА ПАРОЛЬ (`/auth/, /profile/`)
  * реєстрація нового юзера
    * Метод: `POST`
    * URL: `/api/v1/auth/register/`
    * Response Status: `201 Created`
    * Request Body (JSON):
```json
{
  "username": "boardgamer",
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "Тарас",
  "last_name": "Шевченко"
}
```

  * вхід юхера
    * Метод: `POST`
    * URL: `/api/v1/auth/login/`
    * Response Status: `200 OK`
    * Request Body (JSON):
```json
{
  "username": "boardgamer",
  "password": "SecurePassword123!"
}
```
  * Response Body (JSON):
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 5,
  "username": "boardgamer"
}
```

  * перегляд профілю юзера
    * Метод: `GET`
    * URL: `/api/v1/profile/`
    * Headers: `Authorization`
    * Response Status: `200 OK`
    * Response Body (JSON):
```json
{
  "id": 5,
  "username": "boardgamer",
  "email": "user@example.com",
  "first_name": "Тарас",
  "last_name": "Шевченко"
}
```

  * редагуваня своїх даних
    * Метод: `PATCH`
    * URL: `/api/v1/profile/`
    * Headers: `Authorization`
    * Response Status: `200 OK`
    * Request Body (JSON):
```json
{
  "first_name": "Тарас Григорович"
}
```

DATABASE scheme:
<img width="1579" height="382" alt="board_games drawio" src="https://github.com/user-attachments/assets/3883cc4a-c1fd-4ac3-b6f7-73fbc211f377" />


## TODO:
1. Щодо ендпоінтів - кошик юзера `/cart`, історія замовлень `/orders`, сторінка з інформацією `/info`
