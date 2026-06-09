# EduFlow API — Frontend Specification

## Содержание

1. [Общая информация](#1-общая-информация)
2. [Аутентификация](#2-аутентификация)
3. [Модели данных](#3-модели-данных)
4. [Эндпоинты: Auth](#4-эндпоинты-auth)
5. [Эндпоинты: Профиль пользователя](#5-эндпоинты-профиль-пользователя)
6. [Эндпоинты: Подписки](#6-эндпоинты-подписки)
7. [Эндпоинты: Статьи](#7-эндпоинты-статьи)
8. [Эндпоинты: Реакции и сохранения](#8-эндпоинты-реакции-и-сохранения)
9. [Эндпоинты: Комментарии](#9-эндпоинты-комментарии)
10. [Обработка ошибок](#10-обработка-ошибок)
11. [Категории](#11-категории)
12. [Жизненный цикл сессии](#12-жизненный-цикл-сессии)

---

## 1. Общая информация

| Параметр | Значение |
|---|---|
| Base URL | `http://localhost:8080` |
| Формат данных | `application/json` |
| Авторизация | JWT Bearer Token |
| Swagger UI | `http://localhost:8080/swagger-ui.html` |

### Публичные эндпоинты (без токена)

- `POST /auth/signin`
- `POST /auth/signup`
- `POST /auth/refreshtoken`

Все остальные эндпоинты требуют JWT-токен.

---

## 2. Аутентификация

Каждый защищённый запрос должен содержать заголовок:

```
Authorization: Bearer <accessToken>
```

### Схема работы с токенами

```
1. POST /auth/signin → получить accessToken + refreshToken
2. Сохранить оба токена (например, в localStorage)
3. Добавлять accessToken в каждый запрос через заголовок Authorization
4. При получении 401 → POST /auth/refreshtoken с refreshToken → получить новый accessToken
5. При истечении refreshToken → перенаправить на страницу входа
```

### Время жизни токенов

| Токен | TTL |
|---|---|
| Access Token | 10 часов (36 000 000 мс) |
| Refresh Token | 24 часа (86 400 000 мс) |

### Алгоритм подписи

`HS512`

---

## 3. Модели данных

### JwtResponse (ответ при входе/регистрации)

```json
{
  "id": 1,
  "login": "user@example.com",
  "username": "Иван Иванов",
  "role": "ROLE_USER",
  "accessToken": "eyJhbGciOiJIUzUxMiJ9...",
  "type": "Bearer",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

| Поле | Тип | Описание |
|---|---|---|
| `id` | `Long` | ID пользователя |
| `login` | `String` | Логин (email или никнейм) |
| `username` | `String` | Отображаемое имя |
| `role` | `String` | Роль пользователя |
| `accessToken` | `String` | JWT токен для запросов |
| `type` | `String` | Всегда `"Bearer"` |
| `refreshToken` | `String` | UUID токен для обновления |

---

### ProfileResponse (профиль пользователя)

```json
{
  "userId": 1,
  "login": "user@example.com",
  "username": "Иван Иванов",
  "avatar": "https://example.com/avatar.jpg",
  "profile": "Описание профиля",
  "cardDetails": "Дополнительные данные",
  "status": true,
  "userRole": "ROLE_USER",
  "createdAt": "2026-01-15 12:00:00",
  "statusSubscribtion": false
}
```

| Поле | Тип | Описание |
|---|---|---|
| `userId` | `Long` | ID пользователя |
| `login` | `String` | Логин |
| `username` | `String` | Отображаемое имя |
| `avatar` | `String` | URL аватара (может быть `null`) |
| `profile` | `String` | Описание профиля (может быть `null`) |
| `cardDetails` | `String` | Дополнительные сведения (может быть `null`) |
| `status` | `Boolean` | Активен ли аккаунт |
| `userRole` | `String` | Роль: `"ROLE_USER"`, `"ROLE_ADMIN"` и т.д. |
| `createdAt` | `String` | Дата регистрации, формат `"yyyy-MM-dd HH:mm:ss"` |
| `statusSubscribtion` | `Boolean` | Подписан ли **текущий пользователь** на этого |

---

### ArticleResponse (статья)

```json
{
  "currentUserId": 1,
  "articleId": 42,
  "users": { ...ProfileResponse },
  "category": {
    "id": 12,
    "name": "frontend"
  },
  "title": "Заголовок статьи",
  "text": "Полный текст статьи...",
  "description": "Краткое описание",
  "image": "https://example.com/image.jpg",
  "createdAt": "2026-06-09 10:30:00",
  "updatedAt": "2026-06-09 11:00:00",
  "draft": false,
  "statusSave": false,
  "likes": 15,
  "statusLike": true
}
```

| Поле | Тип | Описание |
|---|---|---|
| `currentUserId` | `Long` | ID авторизованного пользователя |
| `articleId` | `Long` | ID статьи |
| `users` | `ProfileResponse` | Автор статьи |
| `category` | `CategoryEntity` | Категория (`id` + `name`) |
| `title` | `String` | Заголовок |
| `text` | `String` | Полный текст (HTML или Markdown) |
| `description` | `String` | Краткое описание |
| `image` | `String` | URL обложки (может быть `null`) |
| `createdAt` | `String` | Дата создания, формат `"yyyy-MM-dd HH:mm:ss"` |
| `updatedAt` | `String` | Дата последнего обновления (может быть `null`) |
| `draft` | `Boolean` | `true` — черновик, `false` — опубликовано |
| `statusSave` | `Boolean` | Сохранена ли статья текущим пользователем |
| `likes` | `Integer` | Количество лайков |
| `statusLike` | `Boolean` | Лайкнул ли текущий пользователь |

---

### CommentResponse (комментарий)

```json
{
  "commentId": 5,
  "article": { ...ArticleResponse },
  "author": { ...ProfileResponse },
  "comment": "Текст комментария"
}
```

| Поле | Тип | Описание |
|---|---|---|
| `commentId` | `Long` | ID комментария |
| `article` | `ArticleResponse` | Статья, к которой относится комментарий |
| `author` | `ProfileResponse` | Автор комментария |
| `comment` | `String` | Текст комментария |

---

### CategoryEntity (категория)

```json
{
  "id": 12,
  "name": "frontend"
}
```

---

### ErrorMessage (ошибка)

```json
{
  "statusCode": 404,
  "message": "Entity Not Found Exception",
  "description": "Entity with id 99 not found",
  "errors": null
}
```

---

## 4. Эндпоинты: Auth

### POST /auth/signup — Регистрация

**Доступ:** публичный

**Request body:**
```json
{
  "login": "user@example.com",
  "password": "securepassword",
  "username": "Иван Иванов",
  "userRole": "ROLE_USER",
  "cardDetails": null,
  "profile": null
}
```

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `login` | `String` | Да | Уникальный логин |
| `password` | `String` | Да | Пароль (хешируется BCrypt) |
| `username` | `String` | Да | Отображаемое имя |
| `userRole` | `String` | Нет | Роль, например `"ROLE_USER"` |
| `cardDetails` | `String` | Нет | Дополнительные данные |
| `profile` | `String` | Нет | Описание профиля |

**Response `200 OK`:** → `JwtResponse` (сразу выполняет вход после регистрации)

**Response `400 Bad Request`:**
```json
{
  "statusCode": 400,
  "message": "Error: Login is already taken!",
  "description": null
}
```

---

### POST /auth/signin — Вход

**Доступ:** публичный

**Request body:**
```json
{
  "login": "user@example.com",
  "password": "securepassword"
}
```

**Response `200 OK`:** → `JwtResponse`

**Response `401 Unauthorized`:** неверные учётные данные

---

### POST /auth/refreshtoken — Обновление access token

**Доступ:** публичный

**Request body:**
```json
{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response `200 OK`:**
```json
{
  "accessToken": "eyJhbGciOiJIUzUxMiJ9...",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "tokenType": "Bearer"
}
```

**Response `403 Forbidden`:** refresh token не найден или истёк

> Если вернулся `403` — refresh token невалиден, нужно перенаправить на страницу входа.

---

## 5. Эндпоинты: Профиль пользователя

Все эндпоинты требуют `Authorization: Bearer <token>`

---

### GET /user/profile — Профиль текущего пользователя

**Response `200 OK`:** → `ProfileResponse`

---

### GET /user/profile/{userId} — Профиль по ID

**Path params:**

| Параметр | Тип | Описание |
|---|---|---|
| `userId` | `Long` | ID пользователя |

**Response `200 OK`:** → `ProfileResponse`

> `statusSubscribtion` в ответе показывает, подписан ли **текущий** авторизованный пользователь на запрошенного.

**Response `404 Not Found`:** пользователь не найден

---

### PUT /user/profile — Обновление профиля

**Request body:** → `ProfileResponse` (только изменяемые поля)

```json
{
  "username": "Новое имя",
  "avatar": "https://example.com/new-avatar.jpg",
  "profile": "Новое описание",
  "cardDetails": "Новые доп. данные"
}
```

> Обновляются только поля: `username`, `avatar`, `profile`, `cardDetails`. Остальные поля игнорируются.

**Response `200 OK`:** → обновлённый `ProfileResponse`

---

## 6. Эндпоинты: Подписки

### POST /user/subscribtion/{userId}?status=true — Подписаться/отписаться

**Path params:**

| Параметр | Тип | Описание |
|---|---|---|
| `userId` | `Long` | ID пользователя, на которого подписываемся |

**Query params:**

| Параметр | Тип | Описание |
|---|---|---|
| `status` | `Boolean` | `true` — подписаться, `false` — отписаться |

**Response `200 OK`:** → `ProfileResponse` пользователя-издателя с актуальным `statusSubscribtion`

**Response `400 Bad Request`:** попытка подписаться на самого себя или повторная подписка/отписка

---

### GET /user/subscribtion — Мои подписки

**Response `200 OK`:** → `List<ProfileResponse>` — список пользователей, на которых подписан текущий пользователь

---

### GET /user/subscribtion/{userId} — Подписки пользователя по ID

**Response `200 OK`:** → `List<ProfileResponse>` — подписки указанного пользователя

---

### GET /user/subscribers — Мои подписчики

**Response `200 OK`:** → `List<ProfileResponse>` — список подписчиков текущего пользователя

---

### GET /user/subscribers/{userId} — Подписчики пользователя по ID

**Response `200 OK`:** → `List<ProfileResponse>` — подписчики указанного пользователя

---

## 7. Эндпоинты: Статьи

### POST /user/article — Создать статью

**Request body:**
```json
{
  "categoryName": "frontend",
  "title": "Заголовок статьи",
  "description": "Краткое описание",
  "text": "Полный текст статьи...",
  "image": "https://example.com/cover.jpg",
  "draft": false
}
```

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `categoryName` | `String` | Да | Точное название категории (чувствительно к регистру) |
| `title` | `String` | Да | Заголовок |
| `description` | `String` | Нет | Краткое описание |
| `text` | `String` | Нет | Полный текст |
| `image` | `String` | Нет | URL обложки |
| `draft` | `Boolean` | Нет | `true` — сохранить как черновик |

**Response `200 OK`:** → `ArticleResponse`

**Response `404 Not Found`:** категория с таким именем не найдена

> Список доступных категорий: `GET /article/category`

---

### PUT /user/article/{articleId}?articleId={id} — Обновить статью

> **Важно:** из-за особенности реализации `articleId` передаётся как **query param**, а не только как path variable.

**URL:** `PUT /user/article/1?articleId=1`

**Request body:** → такой же как при создании (`ArticleRequest`)

```json
{
  "categoryName": "devops",
  "title": "Обновлённый заголовок",
  "description": "Обновлённое описание",
  "text": "Обновлённый текст...",
  "image": "https://example.com/new-cover.jpg",
  "draft": false
}
```

**Response `200 OK`:** → `ArticleResponse`

---

### GET /user/article/{articleId} — Получить статью по ID

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Response `200 OK`:** → `ArticleResponse`

**Response `404 Not Found`:** статья не найдена

---

### GET /user/article — Статьи текущего пользователя

**Response `200 OK`:** → `List<ArticleResponse>` (сортировка: новые первые)

---

### GET /user/article/user/{userId} — Статьи конкретного пользователя

**Path params:**

| Параметр | Тип | Описание |
|---|---|---|
| `userId` | `Long` | ID пользователя-автора |

**Response `200 OK`:** → `List<ArticleResponse>` (сортировка: новые первые)

> `statusSave` и `statusLike` в каждой статье отражают состояние **текущего** авторизованного пользователя, а не автора.

---

### GET /user/article/draft — Черновики текущего пользователя

**Response `200 OK`:** → `List<ArticleResponse>` только с `draft: true`

---

### GET /article — Все статьи (лента)

**Response `200 OK`:** → `List<ArticleResponse>` — все опубликованные статьи

---

### GET /user/subscribtion/article — Статьи из подписок

**Response `200 OK`:** → `List<ArticleResponse>` — статьи всех пользователей, на которых подписан текущий пользователь

---

### GET /user/article/category/{categoryId} — Статьи по категории

**Path params:**

| Параметр | Тип |
|---|---|
| `categoryId` | `Integer` |

**Response `200 OK`:** → `List<ArticleResponse>` (сортировка: новые первые)

**Response `404 Not Found`:** категория не найдена

---

### GET /article/search?line={query} — Поиск статей

**Query params:**

| Параметр | Тип | Описание |
|---|---|---|
| `line` | `String` | Строка поиска по заголовку (регистронезависимый) |

**Response `200 OK`:** → `List<ArticleResponse>`

---

## 8. Эндпоинты: Реакции и сохранения

### POST /user/article/{articleId}/reaction?reaction=true — Поставить/убрать лайк

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Query params:**

| Параметр | Тип | Описание |
|---|---|---|
| `reaction` | `Boolean` | `true` — поставить лайк, `false` — убрать |

**Response `200 OK`:** → `ArticleResponse` с обновлённым `likes` и `statusLike`

**Response `400 Bad Request`:** попытка повторно поставить/убрать лайк

---

### GET /user/article/reaction/count/{articleId} — Количество лайков

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Response `200 OK`:** → `Integer` (число лайков)

---

### POST /user/save/article/{articleId}?status=true — Сохранить/убрать статью

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Query params:**

| Параметр | Тип | Описание |
|---|---|---|
| `status` | `Boolean` | `true` — сохранить, `false` — убрать из сохранённых |

**Response `200 OK`:** → `ArticleResponse` с обновлённым `statusSave`

**Response `400 Bad Request`:** попытка повторно сохранить/убрать

---

### GET /user/saved/articles — Сохранённые статьи

**Response `200 OK`:** → `List<ArticleResponse>`

---

## 9. Эндпоинты: Комментарии

### POST /user/article/{articleId}/comment — Добавить комментарий

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Request body:**
```json
{
  "comment": "Текст комментария"
}
```

**Response `200 OK`:** → `CommentResponse`

---

### GET /user/article/{articleId}/comment — Все комментарии к статье

**Path params:**

| Параметр | Тип |
|---|---|
| `articleId` | `Long` |

**Response `200 OK`:** → `List<CommentResponse>`

---

## 10. Обработка ошибок

Все ошибки возвращают единый формат `ErrorMessage`:

```json
{
  "statusCode": 404,
  "message": "Entity Not Found Exception",
  "description": "Подробное описание ошибки",
  "errors": null
}
```

### Таблица HTTP-статусов

| Статус | Ситуация | Действие на фронтенде |
|---|---|---|
| `400 Bad Request` | Невалидные данные, дубликат действия (лайк уже стоит) | Показать сообщение из `message` |
| `401 Unauthorized` | Токен истёк, невалидный токен | Вызвать `POST /auth/refreshtoken`, при неудаче — редирект на `/login` |
| `403 Forbidden` | Refresh token истёк | Редирект на `/login` |
| `404 Not Found` | Сущность не найдена | Показать страницу 404 |
| `500 Internal Server Error` | Серверная ошибка | Показать общую ошибку |

### Рекомендуемая логика обработки 401

```js
// Псевдокод interceptor'а
async function request(config) {
  try {
    return await fetch(config);
  } catch (error) {
    if (error.status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');
      const response = await fetch('POST /auth/refreshtoken', { refreshToken });
      if (response.ok) {
        localStorage.setItem('accessToken', response.accessToken);
        return await fetch(config); // повторить оригинальный запрос
      } else {
        redirectToLogin();
      }
    }
    throw error;
  }
}
```

---

## 11. Категории

Доступные категории загружаются один раз при старте приложения.

### GET /article/category — Список всех категорий

**Response `200 OK`:**
```json
[
  { "id": 1, "name": "Путешествия" },
  { "id": 2, "name": "Питание" },
  { "id": 3, "name": "Учеба" },
  { "id": 4, "name": "Работа" },
  { "id": 5, "name": "IT сфера" },
  { "id": 6, "name": "Литературоведение" },
  { "id": 7, "name": "Вероисповедание" },
  { "id": 8, "name": "Естественные науки" },
  { "id": 9, "name": "Психология" },
  { "id": 10, "name": "Медицина" },
  { "id": 11, "name": "Остальное" },
  { "id": 12, "name": "frontend" },
  { "id": 13, "name": "qa" },
  { "id": 14, "name": "devops" }
]
```

> При создании/редактировании статьи передаётся **`name`** категории (строка), а не `id`. Значения чувствительны к регистру — использовать точно те строки, что пришли из `/article/category`.

---

## 12. Жизненный цикл сессии

```
Регистрация / Вход
       ↓
  accessToken (10ч) + refreshToken (24ч)
       ↓
  Запросы с Authorization: Bearer <accessToken>
       ↓
  accessToken истёк → 401
       ↓
  POST /auth/refreshtoken → новый accessToken
       ↓
  refreshToken истёк → 403 → редирект на Login
```

### Рекомендации по хранению токенов

| Вариант | Безопасность | Примечание |
|---|---|---|
| `localStorage` | Уязвим к XSS | Прост в реализации |
| `sessionStorage` | Уязвим к XSS | Очищается при закрытии вкладки |
| `httpOnly cookie` | Защищён от XSS | Требует настройки CORS и CSRF на бэкенде |

Текущий бэкенд не устанавливает cookie — токены нужно хранить на стороне клиента и передавать вручную через заголовок `Authorization`.

---

## Сводная таблица всех эндпоинтов

| Метод | URL | Auth | Описание |
|---|---|---|---|
| `POST` | `/auth/signup` | Нет | Регистрация |
| `POST` | `/auth/signin` | Нет | Вход |
| `POST` | `/auth/refreshtoken` | Нет | Обновление токена |
| `GET` | `/user/profile` | Да | Мой профиль |
| `GET` | `/user/profile/{userId}` | Да | Профиль по ID |
| `PUT` | `/user/profile` | Да | Обновить профиль |
| `POST` | `/user/subscribtion/{userId}?status=` | Да | Подписаться/отписаться |
| `GET` | `/user/subscribtion` | Да | Мои подписки |
| `GET` | `/user/subscribtion/{userId}` | Да | Подписки пользователя |
| `GET` | `/user/subscribers` | Да | Мои подписчики |
| `GET` | `/user/subscribers/{userId}` | Да | Подписчики пользователя |
| `POST` | `/user/article` | Да | Создать статью |
| `PUT` | `/user/article/{id}?articleId={id}` | Да | Обновить статью |
| `GET` | `/user/article` | Да | Мои статьи |
| `GET` | `/user/article/{articleId}` | Да | Статья по ID |
| `GET` | `/user/article/user/{userId}` | Да | Статьи пользователя по ID |
| `GET` | `/user/article/draft` | Да | Мои черновики |
| `GET` | `/article` | Да | Все статьи |
| `GET` | `/article/category` | Да | Все категории |
| `GET` | `/article/search?line=` | Да | Поиск статей |
| `GET` | `/user/subscribtion/article` | Да | Лента подписок |
| `GET` | `/user/article/category/{categoryId}` | Да | Статьи по категории |
| `POST` | `/user/article/{articleId}/reaction?reaction=` | Да | Поставить/убрать лайк |
| `GET` | `/user/article/reaction/count/{articleId}` | Да | Кол-во лайков |
| `POST` | `/user/save/article/{articleId}?status=` | Да | Сохранить/убрать статью |
| `GET` | `/user/saved/articles` | Да | Сохранённые статьи |
| `POST` | `/user/article/{articleId}/comment` | Да | Добавить комментарий |
| `GET` | `/user/article/{articleId}/comment` | Да | Комментарии к статье |
