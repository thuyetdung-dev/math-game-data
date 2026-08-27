import streamlit as st
import google.generativeai as genai

# QUAN TRỌNG: Dán API Key của anh vào đây
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="MathGame Creator", page_icon="🎲")
st.title("🎲 Trợ Lý Tạo Game Toán Học THPT")
st.markdown("Chế độ tự chẩn đoán và dò tìm AI")

try:
    # Quét toàn bộ máy chủ Google để tìm các AI mà tài khoản của anh ĐƯỢC PHÉP dùng
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        st.error("API Key đúng, nhưng tài khoản Google này chưa được cấp quyền dùng AI. Anh thử dùng một Gmail khác để tạo API Key nhé.")
    else:
        # Hiển thị menu cho anh tự chọn
        selected_model = st.selectbox("🤖 Hệ thống tìm thấy các AI sau. Anh hãy giữ nguyên hoặc chọn cái khác:", available_models)
        
        with st.form("game_form"):
            topic = st.text_input("📚 Nhập kiến thức trọng tâm của bài học:", placeholder="Ví dụ: Tính đơn điệu...")
            submitted = st.form_submit_button("🚀 Tự động tạo kịch bản Game")

        if submitted and topic:
            with st.spinner(f'Đang kết nối với {selected_model}...'):
                try:
                    model = genai.GenerativeModel(selected_model)
                    prompt = f"""
                    Bạn là một chuyên gia thiết kế game giáo dục. 
                    Kiến thức trọng tâm bài học: "{topic}".
                    Hãy viết hướng dẫn chi tiết tạo trò chơi:
                    - 🎮 TÊN TRÒ CHƠI & CỐT TRUYỆN
                    - 🎨 THIẾT KẾ GIAO DIỆN
                    - 🕹️ CƠ CHẾ GAMEPLAY (Học sinh giải toán thế nào để qua màn?)
                    - 🛠️ NỀN TẢNG THỰC HIỆN
                    """
                    response = model.generate_content(prompt)
                    st.success("🎉 Tạo kịch bản thành công!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Lỗi khi chạy AI: {e}")
                    
except Exception as e:
    st.error(f"Lỗi hệ thống: {e}. Vui lòng kiểm tra lại API Key.")
