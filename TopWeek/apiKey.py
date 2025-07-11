from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')


def api_key():
    return API_KEY
