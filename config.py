import os

class Config:
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key_for_production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    
    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    
    # File Uploads
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Flask-Login Settings
    LOGIN_DISABLED = False
    LOGIN_URL = '/login'
    
    # Logging Configuration
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ENV = 'testing'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}