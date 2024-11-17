## Описание проекта

Этот проект представляет собой RESTful API для управления категориями и продуктами в интернет-магазине. Он позволяет пользователям выполнять операции с товарами, такими как добавление в корзину, изменение количества и удаление товаров из корзины. API также поддерживает авторизацию пользователей с помощью JWT-токенов.

## Стек технологий

- Python 3.12.7
- Django 4.2
- Django REST Framework 3.15.2
- Django MPTT (для иерархии категорий)
- VersatileImageField (для обработки изображений)
- Swagger\Redoc (для документирования API)

## Установка и настройка


1. Клонируйте репозиторий:

```git@github.com:EmpIreR777/TestService.git```

2. Создайте виртуальное окружение и активируйте его:

```python -m venv venv```\
```source venv/Scripts/activate```  - для Windows
```source venv/bin/activate``` - для Linux


3. Установите зависимости:

```python -m pip install --upgrade pip```
```pip install -r requirements.txt```

4. Выполните миграции:

```python manage.py makemigrations```
```python manage.py migrate```

5. Создайте суперпользователя:

```python manage.py createsuperuser```

6. Запустите проект:

```python manage.py runserver```

## Эндпоинты API

### Категории

- Получить все категории:
  - GET ```/api/categories/```
  
- Получить категорию по ID:
  - GET ```/api/categories/{id}/```

### Продукты

- Получить все продукты: 
  - GET ```/api/products/```
  
- Получить продукт по ID:
  - GET ```/api/products/{id}/```

- Добавить продукт в корзину:
  - POST ```/api/products/{id}/shopping_cart/```

- Изменить количество товара в корзине:
  - PUT ```/api/products/{id}/put_shopping_cart/```

- Удалить продукт из корзины:
  - DELETE ```/api/products/{id}/shopping_cart/```

- Проверить состав корзины:
  - GET ```/api/products/list_shopping_cart/```

- Очистить корзину:
  - DELETE ```/api/products/clean_shopping_cart/```

### Авторизация

- Для работы с корзиной пользователь должен быть авторизован. Авторизация осуществляется по JWT-токену.

### Документация

API документируется с помощью Swagger. Чтобы получить доступ к документации, откройте [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/) или
[http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
после запуска сервера.
### Загрузите данные в базу с помощью дампов:
```python manage.py loaddata review/fixtures/products.json```

```python manage.py loaddata review/fixtures/categories.json```

### Автотесты

Проект включает в себя автотесты для некоторых методов (GET и POST). Они помогают убедиться в правильности работы API и его стабильности. Запустить тесты можно с помощью команды:

```python manage.py test```


## Примечания

- Все операции с категориями и продуктами могут выполняться любым пользователем.
- Операции с корзиной могут выполняться только авторизованными пользователями и только с их корзиной.
- Продукты должны обязательно иметь название, slug-имя, изображение в трёх размерах и цену.
- Категории должны содержать наименование, slug-имя, изображение и могут иметь подкатегории.
