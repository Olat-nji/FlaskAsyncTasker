# Flask Application with Celery, RabbitMQ, Nginx, and Ngrok

## Overview

This Flask application demonstrates how to handle background tasks using Celery with RabbitMQ, log time, and serve logs. The application also shows how to handle environment variables, send emails asynchronously, and expose the service using Ngrok.

## Prerequisites

- Python 3.9+
- RabbitMQ
- Nginx
- Ngrok


## Project Structure

```
project
│   app.py           # Main Flask application
│   logger.py        # Logger for logging time
│   tasks.py         # Celery tasks for background processing
│   .env             # Environment variables 
└───requirements.txt # Python Requirements
```

## Environment Variables

Create a `.env` file in the project root and configure the following variables:

```env
# Flask
LOG_FILE_PATH=./logs/app.log

# Celery
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//

# Email
MAIL_HOST=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=your_email@example.com
MAIL_FROM_NAME=Your Name
```

## Installation and Setup

### Step 1: Set Up Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 2: Install Dependencies

Create a `requirements.txt` file in the project root:

```txt
Flask
celery
pytz
python-dotenv
```

Install the dependencies:

```bash
sudo pip install -r requirements.txt
```

### Step 3: Set Up RabbitMQ

Install and start RabbitMQ. On Ubuntu:

```bash
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```

### Step 4: Configure Nginx

Install and configure Nginx. Create an Nginx configuration file for your Flask app (e.g., `flask_app`):

```nginx
server {
    listen 80;

 
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
     location /logs {
        proxy_pass http://127.0.0.1:5000/logs;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        default_type text/plain;
    }
     

}
```

Enable the configuration and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### Step 5: Run Celery Worker

Start the Celery worker:

```bash
celery -A tasks worker --loglevel=info
```

### Step 6: Expose the Service Using Ngrok

Sign up and install Ngrok, then expose the local service:

```bash
ngrok http 80
```

## Running the Flask Application

```bash
sudo python3 app.py
```

## Application Endpoints

- `/` - Main route to handle GET requests. Use query parameters `sendmail` and `talktome` to trigger email sending and log time.
- `/logs` - Route to retrieve log file contents as plaintext.


## Conclusion

This setup demonstrates a way to handle background tasks in a Flask application using Celery with RabbitMQ, with Nginx for reverse proxy, and Ngrok for easy access during development. Ensure all environment variables are properly set and the services (RabbitMQ, Nginx, Celery worker) are running before starting the Flask application.