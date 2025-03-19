import streamlit as st
from utils.tts_service import text_to_speech
import config
import os

def render():
    """Hiển thị trang chuyển văn bản thành giọng nói"""
    # Đầu trang có biểu tượng hấp dẫn
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665184.png", width=60)
    with col2:
        st.header("Chuyển văn bản thành giọng nói")
    
    # Hiển thị các cài đặt hiện tại
    st.info(
        f"🔊 Đang sử dụng: "
        f"{config.LANGUAGE_DISPLAY.get(st.session_state.tts_language, st.session_state.tts_language)} | "
        f"Tốc độ: {st.session_state.tts_speed}x", icon="🎛️"
    )
    
    # Vùng nhập văn bản với placeholder hữu ích
    text_for_speech = st.text_area(
        "Nhập văn bản cần chuyển thành giọng nói",
        height=200,
        placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói tại đây...",
        key="tts_input"
    )
    
    # Nút chuyển đổi đẹp hơn
    col1, col2 = st.columns([3, 1])
    with col1:
        tts_button = st.button("🎤 Chuyển văn bản thành giọng nói", use_container_width=True, type="primary", key="tts_btn")
    with col2:
        clear_button = st.button("🗑️ Xóa", use_container_width=True, key="clear_tts_btn")
        if clear_button:
            st.session_state.text_for_speech = ""
            st.rerun()
    
    # Xử lý khi nhấn nút chuyển đổi
    if tts_button and text_for_speech:
        with st.spinner("Đang chuyển đổi văn bản thành giọng nói..."):
            audio_path = text_to_speech(
                text_for_speech, 
                st.session_state.tts_language, 
                st.session_state.tts_speed
            )
            
            if audio_path:
                # Hiển thị kết quả trong một container đẹp mắt
                result_container = st.container(border=True)
                with result_container:
                    st.subheader("🎵 Kết quả âm thanh")
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Tạo nút tải xuống
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="💾 Tải xuống âm thanh",
                            data=file,
                            file_name="speech.mp3",
                            mime="audio/mp3",
                            use_container_width=True,
                            key="download_tts_btn"
                        )
                    
                    # Hiển thị thông tin về file
                    file_size = os.path.getsize(audio_path) / 1024  # kích thước theo KB
                    st.caption(f"📊 Thông tin: speech.mp3 | {file_size:.1f} KB | "
                              f"{st.session_state.tts_language} | {st.session_state.tts_speed}x")