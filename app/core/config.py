from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve all configuration values from .env
SECRET_KEY = os.getenv('SECRET_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

INITIAL_ADMIN_EMAIL = os.getenv('INITIAL_ADMIN_EMAIL')
INITIAL_ADMIN_PASSWORD = os.getenv('INITIAL_ADMIN_PASSWORD')

INITIAL_STAFF_EMAIL = os.getenv('INITIAL_STAFF_EMAIL')
INITIAL_STAFF_PASSWORD = os.getenv('INITIAL_STAFF_PASSWORD')

INITIAL_USER_EMAIL = os.getenv('INITIAL_USER_EMAIL')
INITIAL_USER_PASSWORD = os.getenv('INITIAL_USER_PASSWORD')

# Set HuggingFace token in environment
os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACEHUB_API_TOKEN
