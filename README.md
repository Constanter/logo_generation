# Logo Generation System

This repository contains a microservices-based system for generating logos based on user inputs.

## Services

- ML Model Service: Generates logos.
- REST API Service: Acts as an intermediary between the client and the ML Model Service.
- Storage Service: Logs all interactions for future analysis and logs marked images.
- Web Interface Service: Provides a graphical interface for users to interact with the system.

## Getting Started

1. Clone the repository.
2. Navigate to the `logo-generation` directory.
3. Copy to the `logo-generation/ml_model_service/data/.cache` model from hugginface `RunDiffusion/Juggernaut-X-Hyper`
3. Run `docker-compose up` to start all services.
4. Access the web interface at `http://localhost:7860`.
5. Acces to the REST API at `http://localhost:5000`

## Инструкция по использованию сервиса:

### Принцип генерации изображения

Для генерации изображения будут использованы парамертры заданные в метаданных. Под капотом метаданные обогащаются промптом. Все изображеиня генерятся в одной цветовой гамме (трех цветах банка - 'светло-лососевый', 'бледно-бирюзовый', 'королевский синий'). Есть возможность задать категорию продукта. Это могут быть либо генерация продающих изображений людей, либо генерации под продукты(машины, дома, кредитные карты). Если задана категория продукта `product` - `people`, то изображения будут генерироваться только с людьми. Можно обогащать промпт с помощью метаданных `custom_prompt`(то что должно еще присутсвовать на изображение).

### Идентификатор пользователя
    - `user_id`: Идентификатор пользователя. Например `Test user`. Может быть любым.


### Метаданные
Метаданные могут содержать следующие поля:

- `sex`: Пол пользователя. Может быть либо 'male' либо 'female' можно оставить пустым.
- `age`: Возраст пользователя. число.
- `product`: Категория продукта. Может быть либо 'people', либо 'car', либо 'house', либо 'credit card' можно оставить пустым.
- `custom_prompt`: Пользовательский промпт. Может быть либо строкой либо пустым. Добавит на генерацию предметы или свойства предметов.
- `height`: Высота изображения. Число. (сумма высоты и ширины должна быть не больше 3500, из-за использования слабой видеокарты.)
- `width`: Ширина изображения. Число. (сумма высоты и ширины должна быть не больше 3500, из-за использования слабой видеокарты.)

### Пример метаданных:
1) 
```
{
    "product": "car",
    "custom_prompt": "engaging in driving",
    "height": 720,
    "width": 720
}
```
2) 
```
{
    "sex": "female",
    "age": 10,
    "height": 480,
    "width": 1160
}
```
3) 
```
{
    "product": "house",
    "custom_prompt": "beautiful country house",
    "height": 1080,
    "width": 1080
}
```

### Генерация изображения

Для генерации изображения необходимо ввести метаданные в поле `metadata` и имя пользователя в поле `user_id` и нажать на кнопку `Generate Image`.

## Разметка изображения

Для разметки изображения необходимо ввести метаданные в поле `metadata` и нажать на кнопку `Generate Image`. После если изображение хоршее и понравилось нажать на кнопку `Mark As Good Image`(выставляется метка True) или оставить чекбокс пустым(False). Отправить изображение в базу данных, нажать на кнопку `Send Mark image to database`.

### Получение истории сгенерированных изображений для пользователя

Ввести в поле `user_id` имя пользователя для которого нужно получить историю и нажать на кнопку `Get History by user ID`. В вверху странице появится таблица с историей сгенерированных изображений для данного пользователя.

## Using the API

To generate an image using the API:

1. Send a POST request to `http://localhost:5000/api/generate` with the user ID in the request body. The API will return the image path and the binary image.
```bash
curl -X POST \
  http://localhost:5000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "123", "metadata": { "age": 20, "sex": "male", "height": 512, "width": 512}}'
```

2. Send a GET request "http://localhost:5000/api/interactions/{user_id}" to get users interactions from database.
```bash
curl -X GET "http://localhost:5000/api/interactions/123"
```

## Dependencies

Each service has its own `requirements.txt` file listing the required Python packages.


## Running the Web Interface

1. Start the Docker containers using `docker-compose up`.
2. Access the web interface at `http://localhost:7860`.


## API examples
```bash
curl -X POST \
  http://localhost:5000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "123", "metadata": { "age": 20, "sex": "male", "height": 512, "width": 512}}'
```


```bash
curl -X GET "http://localhost:5000/api/interactions/123"
```