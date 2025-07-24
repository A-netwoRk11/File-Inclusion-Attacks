# File Inclusion Attacks Demo - Educational Security Platform

🔒 **An educational Django application demonstrating file inclusion vulnerabilities and their defenses.**

⚠️ **WARNING: This application contains intentional vulnerabilities for educational purposes only. Never deploy in production or expose to untrusted networks.**

## 🚀 Quick Start

## 🛠️ Dependencies

- **Python 3.7+**
- **Django 5.2.4**
- **SQLite** (included with Python)

Install dependencies:
```bash
python.exe -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

### Method 1: Using the Enhanced Main Entry Point (Recommended)
```bash
cd "d:\ra1111\Project\File Inclusion Attacks"

# Complete setup (first time only)
python main.py setup

# Start the server
python main.py

# Or start on custom port
python main.py runserver 8080
```

## 📋 Available Commands

The enhanced `main.py` provides a unified interface for all project operations:

```powershell
python main.py                    # Start development server (default)
python main.py runserver          # Start development server
python main.py runserver 8080     # Start server on custom port
python main.py migrate            # Apply database migrations
python main.py makemigrations     # Create new database migrations
python main.py collectstatic      # Collect static files
python main.py shell              # Open Django interactive shell
python main.py createsuperuser    # Create admin superuser account
python main.py test               # Run application tests
python main.py setup              # Complete project setup
python main.py help               # Show help message
```

## 🌐 Demo Endpoints

Once the server is running, access these educational demos:

- **http://127.0.0.1:8000/** - Homepage & Education Hub
- **http://127.0.0.1:8000/lfi** - Local File Inclusion Demo
- **http://127.0.0.1:8000/rfi** - Remote File Inclusion Demo  
- **http://127.0.0.1:8000/payloads** - Attack Payloads Demo
- **http://127.0.0.1:8000/defenses** - Defense Mechanisms
- **http://127.0.0.1:8000/validation** - Input Validation Demo
- **http://127.0.0.1:8000/logs** - Security Logs & Monitoring
- **http://127.0.0.1:8000/tools** - Security Testing Tools
- **http://127.0.0.1:8000/advanced** - Advanced Security Features
- **http://127.0.0.1:8000/secure-demo** - Secure File Access Demo
- **http://127.0.0.1:8000/vulnerability-demo** - Vulnerability Demonstration

## 📚 Educational Features

✅ **Local File Inclusion (LFI) demonstrations**
- Path traversal examples
- Null byte injection
- Wrapper exploitation
- Filter bypass techniques

✅ **Remote File Inclusion (RFI) simulations**
- Remote code execution scenarios
- URL scheme exploitation
- Protocol manipulation

✅ **Security payload examples and analysis**
- Common attack vectors
- Payload construction
- Impact assessment

✅ **Defense mechanisms and mitigation strategies**
- Input validation techniques
- Path canonicalization
- Whitelist implementation
- Security controls

✅ **Security testing tools integration**
- Vulnerability scanners
- Penetration testing tools
- Security assessment frameworks

✅ **Real-time security monitoring and logging**
- Attack detection
- Audit trails
- Incident response`

## 🔒 Security Notes

This application deliberately contains security vulnerabilities for educational purposes:

- **File inclusion vulnerabilities** - Demonstrates LFI/RFI attacks
- **Inadequate input validation** - Shows impact of poor sanitization
- **Insecure file access** - Illustrates path traversal risks
- **Unfiltered user input** - Demonstrates injection vulnerabilities

### 🚨 Important Security Warnings

1. **Never deploy this application in production**
2. **Use only in isolated, controlled environments**
3. **Do not expose to public networks**
4. **Keep it on localhost/internal networks only**
5. **Use for educational purposes only**

## 🎯 Learning Objectives

After using this platform, users should understand:

1. **File inclusion attack vectors and methodologies**
2. **Impact and consequences of file inclusion vulnerabilities**
3. **Effective defense mechanisms and mitigation strategies**
4. **Secure coding practices for file handling**
5. **Security testing tools and techniques**
6. **Real-world vulnerability assessment approaches**

## 🤝 Contributing

This is an educational project. Contributions that enhance the learning experience are welcome:

- Additional vulnerability demonstrations
- Enhanced security explanations
- Improved user interface
- Better documentation
- More comprehensive test cases

## 📄 License

This project is created for EDUCATIONAL PURPOSE ONLY!!. Use responsibly and in compliance with applicable laws and regulations.

**Remember: With great power comes great responsibility. Use this knowledge ethically and only for legitimate security education and testing.**
