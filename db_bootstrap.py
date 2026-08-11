import sys
import subprocess

def install_package(package):
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check dependencies
try:
    import django
except ImportError:
    install_package("django")

try:
    import pymysql
except ImportError:
    install_package("pymysql")

try:
    import cryptography
except ImportError:
    install_package("cryptography")

import pymysql

def create_database():
    connection = None
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8mb4'
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS django_taskflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("Database 'django_taskflow_db' verified/created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}", file=sys.stderr)
        print("Make sure your local MySQL service is running on 127.0.0.1:3306 with user 'root' and no password.", file=sys.stderr)
        sys.exit(1)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_database()
