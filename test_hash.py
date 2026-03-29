import sys
from backend.auth import hash_password

try:
    print("Hashing...", hash_password("test_password" * 10))
    print("Success!")
except Exception as e:
    print("Error:", e)
