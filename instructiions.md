# Instructions for Using the Service
## 1. Using the Service via API
For Developers and Integrators:
To utilize the logo generation service via the API, follow these steps:
API Base URL:
`https://<prod_server>/api`

Generate Image:

```POST https://<prod_server>/api/generate
Request Body:

{
  "user_id": "12345",
  "metadata": {
    "age": 30,
    "sex": "male",
    "height": 512,
    "width": 512
  }
}
Response:

{
  "image_path": "/path/to/image.jpg",
  "image": "base64_encoded_image_string"
}
```
Get Interactions by User ID:
```
GET https://<prod_server>/api/interactions/{user_id}
Response:

[
  {
    "id": 1,
    "user_id": "12345",
    "image_url": "/path/to/image1.jpg",
    "metadata": "{...}"
  },
  ...
]
```
Download All Images by User ID:
```
GET https://<prod_server>/api/download/images/{user_id}
Response:
A ZIP file containing all images associated with the user_id.
```
## 2. Using the Web Interface
For End Users:
To interact with the logo generation service using the web interface:
Visit `https://<prod_server>.`
- Enter your User ID and Metadata in the provided fields.
- Click on "Generate Image".
- View the generated image and mark it as good or bad.
- To view your history, click on "Get History by user ID".
### Setup and Configuration Instructions
Prerequisites:
- Docker and Docker Compose installed on your machine.
- Access to a domain name pointing to your static IP.
Step-by-Step Guide:
- Clone the Repository:
  `git clone https://github.com/Constanter/logo_generation`
- `cd logo_generation`

- `docker-compose build`
  - Start Services: `docker-compose up -d`
Wait for Database:
The services will automatically wait for the database to become available due to the wait_for_db function implemented in each service.
Apply Initial Data Setup:
Run the initial data setup script from the storage_service directory:

docker-compose exec storage_service python src/db.py
Exposing Application on Public IP:
Configure your firewall to allow inbound traffic on ports 5000 and 7860 from your static IP address.

- `sudo ufw allow 5000`
- `sudo ufw allow 7860`
