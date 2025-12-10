##One time converting plain text passwords into hashed passwords

import mysql.connector as db
import hashlib

def get_db():
    return db.connect(
        host="localhost",
        user="selva",
        password="guru",
        database="first_schema"
    )

def hash_password(password):
    """Return SHA-256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

conn = get_db()
cursor = conn.cursor(dictionary=True)

# Get all users
cursor.execute("SELECT username, password_hash FROM userlist")
users = cursor.fetchall()

for user in users:
    plain_pw = user["password_hash"]

    # Skip if already hashed (SHA256 hashes are 64 hex chars)
    if len(plain_pw) == 64 and all(c in "0123456789abcdef" for c in plain_pw.lower()):
        print(f"Skipping {user['username']} (already hashed)")
        continue

    hashed_pw = hash_password(plain_pw)

    cursor.execute(
        "UPDATE userlist SET password_hash=%s WHERE username=%s",
        (hashed_pw, user["username"])
    )

conn.commit()
cursor.close()
conn.close()

