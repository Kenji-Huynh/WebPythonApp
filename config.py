import streamlit as st
from utils.env_utils import load_api_key, save_api_key, remove_api_key

# Dictionary ánh xạ mã ngôn ngữ sang tên hiển thị
LANGUAGE_DISPLAY = {
    "vi": "🇻🇳 Tiếng Việt",
    "en": "🇬🇧 Tiếng Anh",
    "fr": "🇫🇷 Tiếng Pháp",
    "ja": "🇯🇵 Tiếng Nhật",
    "ko": "🇰🇷 Tiếng Hàn",
    "zh-CN": "🇨🇳 Tiếng Trung"
}

def initialize_session_state():
    """Khởi tạo các biến trong session state"""
    # Tải API key từ file .env khi khởi động ứng dụng
    stored_api_key = load_api_key()
    
    default_values = {
        "api_key": stored_api_key,
        "selected_model": "gemini-pro",
        "chat_history": [],
        "tts_language": "vi",
        "tts_speed": 1.0,
        "previous_language": "vi",
        "previous_speed": 1.0
    }
    
    # Khởi tạo tất cả giá trị mặc định nếu chưa tồn tại
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setup_sidebar():
    """Thiết lập sidebar với các cài đặt"""
    with st.sidebar:
        st.image("https://seeklogo.com/images/G/google-ai-logo-996E78F950-seeklogo.com.png", width=100)
        st.title("Cài đặt")
        
        # API Key input với mẫu trợ giúp
        with st.expander("🔑 Google AI API Key", expanded=not st.session_state.api_key):
            api_key = st.text_input(
                "Nhập API Key",
                value=st.session_state.api_key,
                type="password",
                placeholder="",
                key="api_key_input"
            )
            
            # Hiển thị các nút lưu/xóa API key
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Lưu", use_container_width=True, key="save_api_key_btn"):
                    if api_key:
                        if save_api_key(api_key):
                            st.success("✅ API Key đã được lưu")
                    else:
                        st.warning("⚠️ Vui lòng nhập API Key")
            
            with col2:
                if st.button("🗑️ Xóa", use_container_width=True, key="remove_api_key_btn"):
                    if remove_api_key():
                        st.session_state.api_key = ""
                        api_key = ""
                        st.success("✅ API Key đã được xóa")
        
        # Cập nhật API key trong session state
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
        
        # Chọn model với mô tả
        st.divider()
        from utils.ai_service import get_available_models
        models, selected_model = get_available_models(api_key)
        
        st.subheader("🧠 Model AI")
        selected_model = st.selectbox(
            "Chọn model",
            models,
            index=models.index(selected_model) if selected_model in models else 0,
            format_func=lambda x: {
                "gemini-pro": "Gemini Pro (Văn bản)",
                "gemini-pro-vision": "Gemini Pro Vision (Hình ảnh)",
            }.get(x, x),
            key="model_select"
        )
        st.session_state.selected_model = selected_model

        # Lưu cài đặt TTS trước đó
        st.session_state.previous_language = st.session_state.tts_language
        st.session_state.previous_speed = st.session_state.tts_speed
        
        # Cài đặt TTS
        st.divider()
        st.subheader("🔊 Chuyển văn bản thành giọng nói")
        
        # Chọn ngôn ngữ với cờ quốc gia
        tts_language = st.selectbox(
            "Ngôn ngữ",
            options=list(LANGUAGE_DISPLAY.keys()),
            format_func=lambda x: LANGUAGE_DISPLAY.get(x, x),
            index=list(LANGUAGE_DISPLAY.keys()).index(st.session_state.tts_language),
            key="language_select"
        )
        st.session_state.tts_language = tts_language
        
        # Điều chỉnh tốc độ nói
        tts_speed = st.slider(
            "Tốc độ nói", 
            min_value=0.5, 
            max_value=2.0, 
            value=st.session_state.tts_speed, 
            step=0.1,
            format="%.1fx",
            key="speed_slider"
        )
        st.session_state.tts_speed = tts_speed
        
        # Hiển thị thông báo khi thay đổi cài đặt TTS
        if (st.session_state.previous_language != st.session_state.tts_language or 
            st.session_state.previous_speed != st.session_state.tts_speed):
            st.success("✅ Cài đặt giọng nói đã được cập nhật")
            
        # Thêm thông tin phiên bản
        st.divider()
        st.caption("© 2025 Google AI Assistant v1.0")