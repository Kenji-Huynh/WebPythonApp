import streamlit as st
import config
from pages import chat_page, summary_page, tts_page

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

# Thiết lập các tab chức năng với biểu tượng
tab_icons = ["💬", "📝", "🔊"]
tab_names = ["Trò chuyện", "Tóm tắt văn bản", "Chuyển văn bản thành giọng nói"]
tabs = st.tabs([f"{icon} {name}" for icon, name in zip(tab_icons, tab_names)])

# Render các trang chức năng
with tabs[0]:
    chat_page.render()
with tabs[1]:
    summary_page.render()
with tabs[2]:
    tts_page.render()