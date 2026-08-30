import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR/'instance'/'catalogue.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    raw_whatsapp = os.getenv('WHATSAPP_NUMBER', '08037248021').strip()

    if raw_whatsapp.startswith('0'):
        WHATSAPP_NUMBER = '234' + raw_whatsapp[1:]
    elif raw_whatsapp.startswith('234'):
        WHATSAPP_NUMBER = raw_whatsapp
    else:
        WHATSAPP_NUMBER = raw_whatsapp
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-immediately')
    BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL', 'hello@example.com')
    BUSINESS_ADDRESS = os.getenv('BUSINESS_ADDRESS', 'Business address placeholder')
    HERO_VIDEO_URL = os.getenv('HERO_VIDEO_URL', 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4')
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOAD_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
