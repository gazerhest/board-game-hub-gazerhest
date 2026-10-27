# board-game hub - платформа на базі Django REST Framework для інтернет-магазину/ком'юніті настільних ігор. 

## Основний функціонал
+ Каталог настільних ігор - перегляд ігор із пошуком за назвою, фільтрацією за видавництвами, дизайнерами, жанрами/механіками, кількістю гравців, віковими обмеженнями та сортуванням (за ціною, популярністю, рейтингом) і т.д.
+ Картки видавництв та авторів - можливість перегляду каталогу ігор, згрупованих за конкретним українським чи міжнародним видавництвом або автором гри.
+ Автентифікація & профілі - реєстрація, вхід, перегляд/редагування особистих даних юзера.
+ Кошик і замовлення - якщо юзер авторизований, він може додавати товари до кошика, змінювати к-сть та робити замовлення з фіксацією ціни на момент покупки.
+ Адміністративне управління CRUD - create/read/update/delete цих ігор та видавництв і т.д.
+ Загальна інформація - сторінка контактів, правил на доставку, повернення товару.

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

## Ендпоінти
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
