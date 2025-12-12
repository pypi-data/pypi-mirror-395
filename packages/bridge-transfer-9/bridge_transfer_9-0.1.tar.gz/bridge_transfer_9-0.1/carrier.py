
import base64
DATA_B64 = "aW1wb3J0IHFyY29kZQoKZGVmIHR4dF90b19xcl9pbWFnZSh0eHRfZmlsZSwgb3V0cHV0X2ltYWdlPSJxci5wbmciLCBib3hfc2l6ZT01LCBib3JkZXI9Mik6CiAgICAjIMSQ4buNYyBu4buZaSBkdW5nIGZpbGUKICAgIHdpdGggb3Blbih0eHRfZmlsZSwgInIiLCBlbmNvZGluZz0idXRmLTgiKSBhcyBmOgogICAgICAgIGRhdGEgPSBmLnJlYWQoKQoKICAgICMgVOG6oW8gUVIgY29kZQogICAgcXIgPSBxcmNvZGUuUVJDb2RlKAogICAgICAgIHZlcnNpb249Tm9uZSwgICMgxJHhu4MgdOG7sSDEkWnhu4F1IGNo4buJbmggdGhlbyDEkeG7mSBkw6BpIGRhdGEKICAgICAgICBlcnJvcl9jb3JyZWN0aW9uPXFyY29kZS5jb25zdGFudHMuRVJST1JfQ09SUkVDVF9NLAogICAgICAgIGJveF9zaXplPWJveF9zaXplLCAgICMga8OtY2ggdGjGsOG7m2MgbeG7l2kgw7QgKG5o4buPIGjGoW4g4oaSIFFSIG5o4buPIGjGoW4pCiAgICAgICAgYm9yZGVyPWJvcmRlciAgICAgICAgIyB2aeG7gW4gbmdvw6BpCiAgICApCgogICAgcXIuYWRkX2RhdGEoZGF0YSkKICAgIHFyLm1ha2UoZml0PVRydWUpCgogICAgIyBU4bqhbyDhuqNuaAogICAgaW1nID0gcXIubWFrZV9pbWFnZShmaWxsX2NvbG9yPSJibGFjayIsIGJhY2tfY29sb3I9IndoaXRlIikKCiAgICAjIEzGsHUg4bqjbmgKICAgIGltZy5zYXZlKG91dHB1dF9pbWFnZSkKICAgIHByaW50KGYixJDDoyB04bqhbyDhuqNuaCBRUjoge291dHB1dF9pbWFnZX0iKQoKIyBWw60gZOG7pSBkw7luZzoKdHh0X3RvX3FyX2ltYWdlKCJpbnB1dC50eHQiLCAicXIucG5nIiwgYm94X3NpemU9NCwgYm9yZGVyPTIpCg=="
def save(filename="code_moi_ve.py"):
    try:
        decoded = base64.b64decode(DATA_B64).decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(decoded)
        print(f"OK: Da luu code vao {filename}")
    except Exception as e:
        print(f"LOI: {e}")
