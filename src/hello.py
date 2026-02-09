import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

ENV_TYPE = os.getenv('ENV_TYPE', 'development')

if ENV_TYPE == 'production':
    print('Running in production mode')
else:
    print('Running in development mode')
