# Import necessary modules from Flask
from flask import Flask, request, Response

# Import tasks for background processing and logger for logging time
from tasks import send_email
from logger import log_time

# Import os module to work with environment variables
import os

# Load environment variables
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')

# Initialize Flask application
app = Flask(__name__)

# Define main route for handling GET requests
@app.route('/', methods=['GET'])
def main_route():
    # Get query parameters from request URL
    email = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    # Send email task if 'sendmail' parameter is present
    if email:
        send_email.delay(email, 'A test email', 'Just some text')

    # Log time task if 'talktome' parameter is present
    if talktome:
        log_time()

    # Prepare response message
    response = {
        "message": "Action completed"
    }
    return response

# Define route to retrieve log file contents as plaintext
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Attempt to open and read log file
        with open(LOG_FILE_PATH, 'r') as file:
            file_contents = file.read()
        # Return file contents as a plaintext response
        return Response(file_contents, mimetype='text/plain')
    except Exception as e:
        # Return error message and status code 500 if file access fails
        return str(e), 500

# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run()
