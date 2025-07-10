import secrets
import os

key = secrets.token_hex(32)
env_file = '.env'

# Check if .env exists
if not os.path.exists(env_file):
    with open(env_file, 'w') as f:
        f.write(f'FLASK_SECRET_KEY={key}\n')
else:
    # Update or append the key in .env
    lines = []
    updated = False
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('FLASK_SECRET_KEY='):
                lines.append(f'FLASK_SECRET_KEY={key}\n')
                updated = True
            else:
                lines.append(line)
    if not updated:
        lines.append(f'FLASK_SECRET_KEY={key}\n')
    with open(env_file, 'w') as f:
        f.writelines(lines)

print("✅ Secret key added to .env securely!")