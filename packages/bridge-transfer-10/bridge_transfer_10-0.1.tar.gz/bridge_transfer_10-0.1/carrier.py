
import base64
DATA_B64 = "aW1wb3J0IGJhc2U5MQppbXBvcnQgcXJjb2RlCgojIMSQ4buNYyBu4buZaSBkdW5nIGZpbGUgdHh0CndpdGggb3BlbigiaW5wdXQudHh0IiwgInIiLCBlbmNvZGluZz0idXRmLTgiKSBhcyBmOgogICAgdGV4dCA9IGYucmVhZCgpCgojIE7DqW4gJiBtw6MgaMOzYSBi4bqxbmcgQmFzZTkxCmVuY29kZWQgPSBiYXNlOTEuZW5jb2RlKHRleHQuZW5jb2RlKCJ1dGYtOCIpKQoKcHJpbnQoIkJhc2U5MSBlbmNvZGVkOiIpCnByaW50KGVuY29kZWQpCgojIFThuqFvIFFSIGNvZGUgdOG7qyBCYXNlOTEKcXIgPSBxcmNvZGUuUVJDb2RlKAogICAgdmVyc2lvbj1Ob25lLCAgIyBhdXRvIHNpemUKICAgIGVycm9yX2NvcnJlY3Rpb249cXJjb2RlLmNvbnN0YW50cy5FUlJPUl9DT1JSRUNUX00sCiAgICBib3hfc2l6ZT01LCAgICAjIGdp4bqjbSBrw61jaCB0aMaw4bubYyBRUgogICAgYm9yZGVyPTIsCikKCnFyLmFkZF9kYXRhKGVuY29kZWQpCnFyLm1ha2UoZml0PVRydWUpCgppbWcgPSBxci5tYWtlX2ltYWdlKGZpbGxfY29sb3I9ImJsYWNrIiwgYmFja19jb2xvcj0id2hpdGUiKQppbWcuc2F2ZSgicXJfYmFzZTkxLnBuZyIpCnByaW50KCJTYXZlZDogcXJfYmFzZTkxLnBuZyIpCg=="
def save(filename="code_moi_ve.py"):
    try:
        decoded = base64.b64decode(DATA_B64).decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(decoded)
        print(f"OK: Da luu code vao {filename}")
    except Exception as e:
        print(f"LOI: {e}")
