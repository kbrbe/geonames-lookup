# run.py
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine the environment from an environment variable, default to 'development'
env = os.getenv('FLASK_ENV', 'development')

# Create the Flask app instance using the factory function and pass in the environment
app = create_app()

if __name__ == "__main__":
    # Set the host and port from environment variables or use default values
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    
    # Enable debugging mode if environment is development
    debug = (env == 'development')
    
    # Run the Flask app
    app.run(host=host, port=port, debug=debug)
