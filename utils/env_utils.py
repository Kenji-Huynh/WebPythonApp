import os
from dotenv import load_dotenv, set_key, unset_key
import streamlit as st

# Đường dẫn đến file .env
ENV_PATH = ".env"

def load_api_key():
    """
    Tải API key từ file .env nếu tồn tại
    """
    # Tạo file .env nếu nó không tồn tại
    if not os.path.exists(ENV_PATH):
        with open(ENV_PATH, "w") as f:
            pass
    
    # Tải các biến môi trường từ file .env
    load_dotenv(ENV_PATH)
    
    # Lấy API key
    return os.getenv("GOOGLE_AI_API_KEY", "")

def save_api_key(api_key):
    """
    Lưu API key vào file .env
    """
    set_key(ENV_PATH, "GOOGLE_AI_API_KEY", api_key)
    return True

def remove_api_key():
    """
    Xóa API key khỏi file .env
    """
    unset_key(ENV_PATH, "GOOGLE_AI_API_KEY")
    return True