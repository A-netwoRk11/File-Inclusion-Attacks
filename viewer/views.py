from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import logging
import urllib.request
import urllib.parse
from datetime import datetime

# Setup logging for attack attempts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)

BASE_PATH = os.path.abspath("files")  # Only read from /files/

def home(request):
    """Homepage with file inclusion attack awareness article"""
    return render(request, "viewer/index.html")

def vulnerability_demo(request):
    """Main vulnerability demonstration page"""
    return render(request, "viewer/vulnerability_demo.html")

def lfi_demo(request):
    """Local File Inclusion demonstration"""
    mode = request.GET.get('mode', 'secure')  # secure or vulnerable
    filename = request.GET.get('file', '')
    
    context = {
        'mode': mode,
        'filename': filename,
        'demo_type': 'LFI'
    }
    
    if filename:
        # Log the attempt
        client_ip = get_client_ip(request)
        logging.info(f"LFI attempt - IP: {client_ip}, Mode: {mode}, File: {filename}")
        
        if mode == 'vulnerable':
            # VULNERABLE VERSION - DO NOT USE IN PRODUCTION
            try:
                # This is intentionally vulnerable for demonstration
                file_path = os.path.join(BASE_PATH, filename)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                context['content'] = content
                context['success'] = True
            except Exception as e:
                context['error'] = str(e)
        else:
            # SECURE VERSION
            try:
                filepath = os.path.abspath(os.path.join(BASE_PATH, filename))
                if not filepath.startswith(BASE_PATH):
                    context['error'] = "Access denied - Directory traversal detected"
                    logging.warning(f"Directory traversal blocked - IP: {client_ip}, File: {filename}")
                elif not os.path.exists(filepath):
                    context['error'] = "File not found"
                else:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    context['content'] = content
                    context['success'] = True
            except Exception as e:
                context['error'] = f"Error reading file: {str(e)}"
    
    return render(request, "viewer/lfi_demo.html", context)

def rfi_demo(request):
    """Remote File Inclusion demonstration"""
    mode = request.GET.get('mode', 'secure')
    url = request.GET.get('url', '')
    
    context = {
        'mode': mode,
        'url': url,
        'demo_type': 'RFI'
    }
    
    if url:
        client_ip = get_client_ip(request)
        logging.info(f"RFI attempt - IP: {client_ip}, Mode: {mode}, URL: {url}")
        
        if mode == 'vulnerable':
            # VULNERABLE VERSION - DO NOT USE IN PRODUCTION
            try:
                # This is intentionally vulnerable for demonstration
                response = urllib.request.urlopen(url, timeout=5)
                content = response.read().decode('utf-8')
                context['content'] = content
                context['success'] = True
            except Exception as e:
                context['error'] = str(e)
        else:
            # SECURE VERSION
            context['error'] = "Remote file inclusion is disabled for security"
            logging.warning(f"RFI attempt blocked - IP: {client_ip}, URL: {url}")
    
    return render(request, "viewer/rfi_demo.html", context)

def payloads_demo(request):
    """Attack payload examples"""
    return render(request, "viewer/payloads_demo.html")

def defense_mechanisms(request):
    """Defense mechanisms demonstration"""
    return render(request, "viewer/defense_mechanisms.html")

def security_logs(request):
    """View security logs"""
    try:
        with open('security.log', 'r') as f:
            logs = f.readlines()
        # Get last 50 logs
        logs = logs[-50:]
        return render(request, "viewer/security_logs.html", {'logs': logs})
    except FileNotFoundError:
        return render(request, "viewer/security_logs.html", {'logs': []})

def input_validation_demo(request):
    """Input validation demonstration"""
    input_text = request.GET.get('input', '')
    validation_type = request.GET.get('type', 'basic')
    
    context = {
        'input_text': input_text,
        'validation_type': validation_type
    }
    
    if input_text:
        client_ip = get_client_ip(request)
        logging.info(f"Input validation test - IP: {client_ip}, Type: {validation_type}, Input: {input_text}")
        
        if validation_type == 'basic':
            # Basic validation
            if '../' in input_text or '..\\' in input_text:
                context['result'] = 'BLOCKED: Directory traversal detected'
                context['blocked'] = True
            elif input_text.startswith(('http://', 'https://', 'ftp://')):
                context['result'] = 'BLOCKED: URL detected'
                context['blocked'] = True
            else:
                context['result'] = 'ALLOWED: Input appears safe'
                context['blocked'] = False
        
        elif validation_type == 'advanced':
            # Advanced validation with regex
            import re
            dangerous_patterns = [
                r'\.\.[\\/]',  # Directory traversal
                r'[a-zA-Z]+:\/\/',  # URLs
                r'[<>"\']',  # HTML/SQL injection chars
                r'[\x00-\x1f\x7f-\x9f]',  # Control characters
            ]
            
            blocked = False
            for pattern in dangerous_patterns:
                if re.search(pattern, input_text):
                    context['result'] = f'BLOCKED: Dangerous pattern detected: {pattern}'
                    context['blocked'] = True
                    blocked = True
                    break
            
            if not blocked:
                context['result'] = 'ALLOWED: Input passed advanced validation'
                context['blocked'] = False
        
        elif validation_type == 'whitelist':
            # Whitelist validation
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-')
            if all(c in allowed_chars for c in input_text):
                context['result'] = 'ALLOWED: Input contains only whitelisted characters'
                context['blocked'] = False
            else:
                context['result'] = 'BLOCKED: Input contains non-whitelisted characters'
                context['blocked'] = True
    
    return render(request, "viewer/input_validation_demo.html", context)

def view_file(request):
    """Original file viewer for backward compatibility"""
    filename = request.GET.get("file")
    
    if not filename:
        return render(request, "viewer/view_file.html", {"error": "No file specified"})
    
    try:
        filepath = os.path.abspath(os.path.join(BASE_PATH, filename))
        if not filepath.startswith(BASE_PATH):
            return render(request, "viewer/view_file.html", {"error": "Access denied - Directory traversal detected"})
        
        if not os.path.exists(filepath):
            return render(request, "viewer/view_file.html", {"error": "File not found"})
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        return render(request, "viewer/view_file.html", {"content": content, "filename": filename})
    
    except Exception as e:
        return render(request, "viewer/view_file.html", {"error": f"Error reading file: {str(e)}"})

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# SECURE FILE HANDLING - BEST PRACTICES IMPLEMENTATION
# This section demonstrates the recommended approaches to prevent file inclusion attacks

# 1. WHITELIST APPROACH - Only allow predefined files
ALLOWED_FILES = {
    'welcome': {
        'file': 'sample.txt',
        'title': 'Welcome Message',
        'description': 'Sample welcome text file'
    },
    'config': {
        'file': 'config.txt',
        'title': 'Configuration Example',
        'description': 'Sample configuration file (educational)'
    },
    'logs': {
        'file': 'application.log',
        'title': 'Application Logs',
        'description': 'Sample application log file'
    },
    'users': {
        'file': 'users.csv',
        'title': 'User Data',
        'description': 'Sample user database (educational)'
    },
    'readme': {
        'file': 'readme.txt',
        'title': 'Documentation',
        'description': 'Project documentation'
    }
}

# 2. ALTERNATIVE INPUT SOURCES - Demonstrate secure alternatives
SECURE_FILE_CATEGORIES = {
    'documentation': ['readme', 'welcome'],
    'configuration': ['config'],
    'monitoring': ['logs'],
    'data': ['users']
}

# 3. SECURITY TESTING TOOLS INFORMATION
SECURITY_TESTING_TOOLS = {
    'static_analysis': {
        'invicti': {
            'name': 'Invicti (Netsparker)',
            'description': 'Web application security scanner',
            'features': ['Automated vulnerability scanning', 'False positive reduction', 'Integration with CI/CD']
        },
        'acunetix': {
            'name': 'Acunetix',
            'description': 'Web vulnerability scanner',
            'features': ['OWASP Top 10 coverage', 'Authentication testing', 'REST API security']
        },
        'veracode': {
            'name': 'Veracode',
            'description': 'Static and dynamic analysis',
            'features': ['Source code analysis', 'Binary analysis', 'Software composition analysis']
        }
    },
    'dynamic_analysis': {
        'burp_suite': {
            'name': 'Burp Suite',
            'description': 'Web application security testing',
            'features': ['Manual testing', 'Automated scanning', 'Extensible platform']
        },
        'owasp_zap': {
            'name': 'OWASP ZAP',
            'description': 'Free security testing proxy',
            'features': ['Automated scanning', 'Manual testing', 'API testing']
        }
    },
    'code_review': {
        'sonarqube': {
            'name': 'SonarQube',
            'description': 'Code quality and security analysis',
            'features': ['Security hotspots', 'Code smells', 'Technical debt']
        },
        'checkmarx': {
            'name': 'Checkmarx',
            'description': 'Static application security testing',
            'features': ['Source code analysis', 'Open source scanning', 'Supply chain security']
        }
    }
}

def secure_file_demo(request):
    """Demonstration of secure file handling using best practices"""
    file_id = request.GET.get('file_id', '')
    method = request.GET.get('method', 'whitelist')
    
    context = {
        'file_id': file_id,
        'method': method,
        'allowed_files': ALLOWED_FILES,
        'file_categories': SECURE_FILE_CATEGORIES
    }
    
    if file_id:
        client_ip = get_client_ip(request)
        logging.info(f"Secure file access - IP: {client_ip}, Method: {method}, File ID: {file_id}")
        
        if method == 'whitelist':
            # METHOD 1: WHITELIST APPROACH
            if file_id in ALLOWED_FILES:
                try:
                    file_info = ALLOWED_FILES[file_id]
                    filepath = os.path.join(BASE_PATH, file_info['file'])
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    context['content'] = content
                    context['file_info'] = file_info
                    context['success'] = True
                    
                except Exception as e:
                    context['error'] = f"Error reading file: {str(e)}"
            else:
                context['error'] = f"File ID '{file_id}' not found in whitelist"
                logging.warning(f"Unauthorized file access attempt - IP: {client_ip}, File ID: {file_id}")
        
        elif method == 'switch_case':
            # METHOD 2: SWITCH/CASE PATTERN
            context['content'], context['file_info'], context['error'] = handle_file_by_case(file_id, client_ip)
            if context['content']:
                context['success'] = True
        
        elif method == 'category_based':
            # METHOD 3: CATEGORY-BASED ACCESS
            category = request.GET.get('category', '')
            if category in SECURE_FILE_CATEGORIES and file_id in SECURE_FILE_CATEGORIES[category]:
                if file_id in ALLOWED_FILES:
                    try:
                        file_info = ALLOWED_FILES[file_id]
                        filepath = os.path.join(BASE_PATH, file_info['file'])
                        
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        context['content'] = content
                        context['file_info'] = file_info
                        context['success'] = True
                        context['category'] = category
                        
                    except Exception as e:
                        context['error'] = f"Error reading file: {str(e)}"
                else:
                    context['error'] = "File not found in system"
            else:
                context['error'] = "Invalid category or file not allowed in this category"
                logging.warning(f"Category-based access denied - IP: {client_ip}, Category: {category}, File: {file_id}")
    
    return render(request, "viewer/secure_file_demo.html", context)

def handle_file_by_case(file_id, client_ip):
    """Switch/Case pattern for file handling - more secure than dynamic paths"""
    
    # This mimics a switch/case statement using if-elif
    if file_id == 'welcome':
        filepath = os.path.join(BASE_PATH, 'sample.txt')
        file_info = ALLOWED_FILES['welcome']
    elif file_id == 'config':
        filepath = os.path.join(BASE_PATH, 'config.txt')
        file_info = ALLOWED_FILES['config']
    elif file_id == 'logs':
        filepath = os.path.join(BASE_PATH, 'application.log')
        file_info = ALLOWED_FILES['logs']
    elif file_id == 'users':
        filepath = os.path.join(BASE_PATH, 'users.csv')
        file_info = ALLOWED_FILES['users']
    elif file_id == 'readme':
        # Create readme file if it doesn't exist
        readme_path = os.path.join(BASE_PATH, 'readme.txt')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as f:
                f.write("# File Inclusion Security Demo\n\nThis is a secure file access demonstration.\n\nFeatures:\n- Whitelist-based file access\n- Switch/case pattern implementation\n- Security testing integration\n\nEducational purpose only!")
        filepath = readme_path
        file_info = ALLOWED_FILES['readme']
    else:
        # Invalid file ID - log the attempt
        logging.warning(f"Switch-case access denied - IP: {client_ip}, Invalid File ID: {file_id}")
        return None, None, f"File ID '{file_id}' is not supported"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, file_info, None
    except Exception as e:
        return None, None, f"Error reading file: {str(e)}"

def security_testing_tools(request):
    """Information about security testing tools and methodologies"""
    tool_category = request.GET.get('category', 'all')
    
    context = {
        'tool_category': tool_category,
        'security_tools': SECURITY_TESTING_TOOLS,
        'all_tools': tool_category == 'all'
    }
    
    if tool_category != 'all' and tool_category in SECURITY_TESTING_TOOLS:
        context['selected_tools'] = SECURITY_TESTING_TOOLS[tool_category]
    
    return render(request, "viewer/security_testing_tools.html", context)

def advanced_security_demo(request):
    """Advanced security demonstration combining all best practices"""
    return render(request, "viewer/advanced_security_demo.html", {
        'allowed_files': ALLOWED_FILES,
        'file_categories': SECURE_FILE_CATEGORIES,
        'security_tools': SECURITY_TESTING_TOOLS
    })
