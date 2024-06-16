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