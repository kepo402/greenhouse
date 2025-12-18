import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenhouse.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
