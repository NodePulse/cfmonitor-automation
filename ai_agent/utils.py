import os


def ensure_dirs():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("results", exist_ok=True)
