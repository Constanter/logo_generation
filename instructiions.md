Instructions for Using the Service
1. Using the Service via API
For Developers and Integrators:
To utilize the logo generation service via the API, follow these steps:
API Base URL:
`https://yourdomain.com/api`

Generate Image:

POST https://yourdomain.com/api/generate
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
Get Interactions by User ID:

GET https://yourdomain.com/api/interactions/{user_id}
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
Download All Images by User ID:

GET https://yourdomain.com/api/download/images/{user_id}
Response:
A ZIP file containing all images associated with the user_id.
2. Using the Web Interface
For End Users:
To interact with the logo generation service using the web interface:
Visit https://yourdomain.com.
Enter your User ID and Metadata in the provided fields.
Click on "Generate Image".
View the generated image and mark it as good or bad.
To view your history, click on "Get History by user ID".
Setup and Configuration Instructions
Prerequisites:
Docker and Docker Compose installed on your machine.
Access to a domain name pointing to your static IP (88.19.31.0).
Step-by-Step Guide:
Clone the Repository:

git clone https://github.com/yourusername/logo-generation-service.git
cd logo-generation-service
Set Up Environment Variables:
Create .env files in each service directory (ml_model_service, rest_api_service, storage_service, web_interface_service) with the following content:

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=logo_storage
Build Docker Images:

docker-compose build
Start Services:

docker-compose up -d
Wait for Database:
The services will automatically wait for the database to become available due to the wait_for_db function implemented in each service.
Apply Initial Data Setup:
Run the initial data setup script from the storage_service directory:

docker-compose exec storage_service python src/db.py
Exposing Application on Public IP:
Configure your firewall to allow inbound traffic on ports 5000 and 7860 from your static IP address (88.19.31.0).

sudo ufw allow from 88.19.31.0 to any port 5000
sudo ufw allow from 88.19.31.0 to any port 7860
DNS Configuration:
Update your domain registrar's DNS settings to point your domain to the static IP address (88.19.31.0).
Access the Service:
The API endpoints will be accessible at https://yourdomain.com/api.
The web interface will be accessible at https://yourdomain.com.
Additional Tips:
SSL/TLS Certificate:
Obtain an SSL/TLS certificate from a trusted provider or use Let's Encrypt.
Update your nginx configuration to redirect HTTP to HTTPS and terminate SSL/TLS at the reverse proxy level.
Monitoring and Logging:
Implement centralized logging and monitoring solutions like ELK Stack or Prometheus and Grafana.
Configure alerting for critical system events.
Security Best Practices:
Regularly update dependencies and patch vulnerabilities.
Implement rate limiting and DDoS protection.
Enable access logs and review them regularly.
By following these instructions, you can set up, configure, and run the logo generation service on your static IP address, making it accessible to users via both the API and the web interface. Ensure that you maintain regular backups and updates to keep the system secure and compliant with industry standards.
