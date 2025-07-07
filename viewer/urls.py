from django.urls import path
from .views import (
    home, view_file, vulnerability_demo, lfi_demo, rfi_demo, 
    payloads_demo, defense_mechanisms, security_logs, input_validation_demo,
    secure_file_demo, security_testing_tools, advanced_security_demo
)

urlpatterns = [
    path('', home, name='home'),
    path('view/', view_file, name='view_file'),
    path('demo/', vulnerability_demo, name='vulnerability_demo'),
    
    # Short URLs for easy access (as shown in main.py)
    path('lfi/', lfi_demo, name='lfi_demo_short'),
    path('rfi/', rfi_demo, name='rfi_demo_short'),
    path('payloads/', payloads_demo, name='payloads_demo_short'),
    path('defenses/', defense_mechanisms, name='defense_mechanisms_short'),
    path('validation/', input_validation_demo, name='input_validation_demo_short'),
    path('secure-demo/', secure_file_demo, name='secure_file_demo_short'),
    path('advanced/', advanced_security_demo, name='advanced_security_demo_short'),
    path('vulnerability-demo/', vulnerability_demo, name='vulnerability_demo_short'),
    path('tools/', security_testing_tools, name='security_testing_tools'),
    path('logs/', security_logs, name='security_logs'),
    
    # Original longer URLs (for backward compatibility)
    path('demo/lfi/', lfi_demo, name='lfi_demo'),
    path('demo/rfi/', rfi_demo, name='rfi_demo'),
    path('demo/payloads/', payloads_demo, name='payloads_demo'),
    path('demo/defense/', defense_mechanisms, name='defense_mechanisms'),
    path('demo/validation/', input_validation_demo, name='input_validation_demo'),
    path('demo/secure-file/', secure_file_demo, name='secure_file_demo'),
    path('demo/advanced/', advanced_security_demo, name='advanced_security_demo'),
]
