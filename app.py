import streamlit as st
import config
from utils.ai_service import get_ai_response
from utils.tts_service import text_to_speech

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Google AI Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo session state và thiết lập sidebar
config.initialize_session_state()
config.setup_sidebar()

def render_chat():
    """Hiển thị giao diện trò chuyện"""
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665038.png", width=60)
    with col2:
        st.header("Trò chuyện với AI")
    
    if not st.session_state.api_key:
        st.info("🔑 Vui lòng nhập Google AI API Key trong phần cài đặt để bắt đầu trò chuyện", icon="ℹ️")
        st.divider()
    
    for message in st.session_state.chat_history:
        role_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=role_icon):
            st.markdown(message["content"])
    
    user_input = st.chat_input("Nhập câu hỏi của bạn...", key="chat_input")
    
    if user_input:
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi gửi tin nhắn", icon="🔒")
            return
            
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)
        
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang suy nghĩ..."):
                response = get_ai_response(
                    user_input, 
                    st.session_state.selected_model, 
                    st.session_state.api_key
                )
                st.markdown(response)
        
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": response
        })
    
    if st.session_state.chat_history:
        if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True, key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()

def render_summary():
    """Hiển thị giao diện tóm tắt văn bản"""
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665184.png", width=60)
    with col2:
        st.header("Tóm tắt văn bản")
    
    text_to_summarize = st.text_area(
        "Nhập văn bản cần tóm tắt",
        height=200,
        placeholder="Dán văn bản cần tóm tắt vào đây...",
        key="summary_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.select_slider(
            "Độ dài",
            options=["Rất ngắn", "Ngắn", "Trung bình", "Dài", "Chi tiết"],
            value="Trung bình",
            key="summary_length"
        )
    with col2:
        summary_style = st.radio(
            "Phong cách",
            options=["Tóm lược", "Điểm chính", "Phân tích"],
            horizontal=True,
            key="summary_style"
        )
    
    summarize_button = st.button("📝 Tóm tắt ngay", use_container_width=True, type="primary", key="summarize_btn")
    
    if summarize_button:
        if not text_to_summarize:
            st.warning("⚠️ Vui lòng nhập văn bản cần tóm tắt", icon="📄")
            return
            
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi sử dụng tính năng này", icon="🔒")
            return
            
        with st.spinner("AI đang tóm tắt văn bản..."):
            prompt = f"""Hãy tóm tắt văn bản sau với độ dài {summary_length.lower()} 
            theo phong cách {summary_style.lower()}. Đảm bảo giữ lại các ý chính và 
            bỏ qua các chi tiết không quan trọng:\n\n{text_to_summarize}"""
            
            summary = get_ai_response(
                prompt, 
                st.session_state.selected_model, 
                st.session_state.api_key
            )
            
            st.success("✅ Tạo bản tóm tắt thành công!")
            result_container = st.container(border=True)
            with result_container:
                st.subheader("📋 Bản tóm tắt")
                st.markdown(summary)
                
                st.download_button(
                    label="📄 Tải xuống văn bản",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_text_btn"
                )

def render_tts():
    """Hiển thị giao diện chuyển văn bản thành giọng nói"""
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665184.png", width=60)
    with col2:
        st.header("Chuyển văn bản thành giọng nói")
    
    st.info(
        f"🔊 Đang sử dụng: "
        f"{config.LANGUAGE_DISPLAY.get(st.session_state.tts_language, st.session_state.tts_language)} | "
        f"Tốc độ: {st.session_state.tts_speed}x", icon="🎛️"
    )
    
    text_for_speech = st.text_area(
        "Nhập văn bản cần chuyển thành giọng nói",
        height=200,
        placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói tại đây...",
        key="tts_input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        tts_button = st.button("🎤 Chuyển văn bản thành giọng nói", use_container_width=True, type="primary", key="tts_btn")
    with col2:
        clear_button = st.button("🗑️ Xóa", use_container_width=True, key="clear_tts_btn")
        if clear_button:
            st.session_state.text_for_speech = ""
            st.rerun()
    
    if tts_button and text_for_speech:
        with st.spinner("Đang chuyển đổi văn bản thành giọng nói..."):
            audio_path = text_to_speech(
                text_for_speech, 
                st.session_state.tts_language, 
                st.session_state.tts_speed
            )
            
            if audio_path:
                result_container = st.container(border=True)
                with result_container:
                    st.subheader("🎵 Kết quả âm thanh")
                    st.audio(audio_path, format="audio/mp3")
                    
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="💾 Tải xuống âm thanh",
                            data=file,
                            file_name="speech.mp3",
                            mime="audio/mp3",
                            use_container_width=True,
                            key="download_tts_btn"
                        )

# Thiết lập các tab chức năng với biểu tượng
tab_icons = ["💬", "📝", "🔊"]
tab_names = ["Trò chuyện", "Tóm tắt văn bản", "Chuyển văn bản thành giọng nói"]
tabs = st.tabs([f"{icon} {name}" for icon, name in zip(tab_icons, tab_names)])

# Render các trang chức năng dựa trên tab được chọn
with tabs[0]:
    render_chat()
with tabs[1]:
    render_summary()
with tabs[2]:
    render_tts()