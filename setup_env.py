import secrets
import os

env_file = '.env'
secret_key = secrets.token_hex(32)

# Credentials – update these before running!
your_email = 'saimanikantabamini@gmail.com'
app_password = 'merf zylk wkxf mlrd'  # App-specific password, NOT your main Gmail password

# Key-Value pairs to write
env_vars = {
    'FLASK_SECRET_KEY': secret_key,
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': '587',
    'MAIL_USE_TLS': 'True',
    'MAIL_USERNAME': your_email,
    'MAIL_PASSWORD': app_password
}

# Create or update .env
if not os.path.exists(env_file):
    with open(env_file, 'w') as f:
        for key, value in env_vars.items():
            f.write(f'{key}={value}\n')
else:
    # Update existing keys or append new ones
    with open(env_file, 'r') as f:
        lines = f.readlines()

    updated_keys = set()
    new_lines = []
    for line in lines:
        key = line.split('=')[0].strip()
        if key in env_vars:
            new_lines.append(f'{key}={env_vars[key]}\n')
            updated_keys.add(key)
        else:
            new_lines.append(line)

    # Add missing keys
    for key, value in env_vars.items():
        if key not in updated_keys:
            new_lines.append(f'{key}={value}\n')

    with open(env_file, 'w') as f:
        f.writelines(new_lines)

print("✅ .env file has been updated with secure keys and email config!")