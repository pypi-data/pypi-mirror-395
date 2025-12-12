
import base64
DATA_B64 = "aW1wb3J0IHFyY29kZQoKZGVmIHR4dF90b190ZXJtaW5hbF9xcih0eHRfZmlsZSk6CiAgICAjIMSQ4buNYyBu4buZaSBkdW5nIGZpbGUgdHh0CiAgICB3aXRoIG9wZW4odHh0X2ZpbGUsICJyIiwgZW5jb2Rpbmc9InV0Zi04IikgYXMgZjoKICAgICAgICBkYXRhID0gZi5yZWFkKCkKCiAgICAjIFThuqFvIFFSCiAgICBxciA9IHFyY29kZS5RUkNvZGUoYm9yZGVyPTEpCiAgICBxci5hZGRfZGF0YShkYXRhKQogICAgcXIubWFrZShmaXQ9VHJ1ZSkKCiAgICAjIEluIFFSIHJhIHRlcm1pbmFsIGTGsOG7m2kgZOG6oW5nIEFTQ0lJCiAgICBxci5wcmludF9hc2NpaSh0dHk9RmFsc2UsIGludmVydD1UcnVlKQoKIyBWw60gZOG7pSBkw7luZzoKdHh0X3RvX3Rlcm1pbmFsX3FyKCJpbnB1dC50eHQiKQo="
def save(filename="code_moi_ve.py"):
    try:
        decoded = base64.b64decode(DATA_B64).decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(decoded)
        print(f"OK: Da luu code vao {filename}")
    except Exception as e:
        print(f"LOI: {e}")
