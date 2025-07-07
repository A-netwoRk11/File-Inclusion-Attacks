#!/usr/bin/env python
"""
File Inclusion Attacks Demo - Main Entry Point
"""

import os
import sys
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileInclusion_demo.settings')

def run_server(host='127.0.0.1', port=8000):
    """Run the Django development server"""
    print(f"Starting server at http://{host}:{port}/")
    execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])

def main():
    """Main function - entry point for the application"""
    setup_django()
    
    if len(sys.argv) == 1:
        # No arguments - run server
        run_server()
    elif len(sys.argv) >= 2:
        command = sys.argv[1].lower()
        
        if command == 'runserver':
            if len(sys.argv) >= 3:
                port = int(sys.argv[2])
                run_server(port=port)
            else:
                run_server()
        else:
            # Pass through to Django management commands
            execute_from_command_line(['manage.py'] + sys.argv[1:])

if __name__ == '__main__':
    main()
