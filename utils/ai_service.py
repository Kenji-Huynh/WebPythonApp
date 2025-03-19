import google.generativeai as genai
import streamlit as st

def get_available_models(api_key):
    """Lấy danh sách các model có sẵn từ Google AI API"""
    if api_key:
        genai.configure(api_key=api_key)
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            selected_model = models[0] if models else "gemini-pro"
            return models, selected_model
        except Exception as e:
            st.sidebar.error(f"Lỗi khi kết nối API: {str(e)}")
    
    # Trường hợp không có API key hoặc có lỗi
    return ["gemini-pro"], "gemini-pro"

def get_ai_response(prompt, model_name, api_key):
    """Tạo phản hồi từ AI"""
    if not api_key:
        return "Vui lòng nhập API Key từ Google AI Studio trong phần cài đặt."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"