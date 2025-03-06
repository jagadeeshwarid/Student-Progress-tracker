import hashlib

new_password = "ansir123"  # Replace with your new password
hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

print("New Hashed Password:", hashed_password)
