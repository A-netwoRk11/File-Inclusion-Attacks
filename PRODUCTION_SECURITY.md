# Production-Ready Security Settings (If you must deploy)

# settings.py changes:
DEBUG = False  # In Production always False
ALLOWED_HOSTS = ['yourdomain.com']  # Specific domain only
SECRET_KEY = 'your-very-strong-secret-key-here'

# Disable vulnerable modes:
ENABLE_VULNERABLE_MODE = False  # False in Production

# Add security headers:
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000

# Database security:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Secure database
        'NAME': 'secure_db_name',
        'USER': 'secure_user',
        'PASSWORD': 'very_strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
