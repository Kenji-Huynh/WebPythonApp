import streamlit as st
from gtts import gTTS
import tempfile

def text_to_speech(text, lang="vi", speed=1.0):
    """Chuyển văn bản thành giọng nói và trả về đường dẫn file tạm"""
    try:
        tts = gTTS(text=text, lang=lang, slow=(speed < 1.0))
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file = fp.name
            
        tts.save(temp_file)
        
        return temp_file
    except Exception as e:
        st.error(f"Lỗi khi chuyển đổi văn bản thành giọng nói: {str(e)}")
        return None