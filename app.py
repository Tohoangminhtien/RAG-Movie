import streamlit as st
from dotenv import load_dotenv
import os
from chat import ChatbotAI

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
user_name = os.getenv("USER_NAME")
neo4j_url = os.getenv("URL")
database = os.getenv("DATABASE")
password = os.getenv("PASSWORD")

chatbot = ChatbotAI(open_ai_key=open_ai_key, user_name=user_name,
                    neo4j_url=neo4j_url, database=database, password=password)

st.set_page_config(page_title="Movie 🎬 Assistant", layout="wide")

st.markdown("""
    <style>
        /* Nền với hình PNG */
        .stApp {
            background: url('https://cdn-icons-png.flaticon.com/512/24/24789.png') no-repeat center center fixed;
            background-size: cover;
            background-attachment: fixed;
        }

        /* Tùy chỉnh khung chat */
        .stChatMessage {
            max-width: 70%;
            margin: 15px auto;
            border-radius: 20px;
            padding: 15px 20px;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;`
            word-wrap: break-word; /* Đảm bảo nội dung tin nhắn không bị tràn */
            font-family: 'Arial', sans-serif;
        }

        /* Hiệu ứng hover cho khung chat */
        .stChatMessage:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
        }

        /* Khung chat người dùng */
        .stChatMessageUser {
            background-color: rgba(79, 70, 229, 0.9);
            color: white;
            align-self: flex-end; /* Căn phải */
            border-top-right-radius: 0;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        }

        /* Khung chat trợ lý */
        .stChatMessageAssistant {
            background-color: rgba(255, 87, 34, 0.9);
            color: white;
            align-self: flex-start; /* Căn trái */
            border-top-left-radius: 0;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        }

        /* Khoảng cách giữa các tin nhắn */
        .stChatMessage + .stChatMessage {
            margin-top: 25px;
        }

        /* Căn chỉnh container chat để các tin nhắn nằm 2 bên */
        .stChatMessage {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        /* Footer */
        .footer {
            font-size: 14px;
            color: #777;
            text-align: center;
            margin-top: 50px;
            padding: 10px;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: #2d2d2d;
            color: #fff;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎬 **Movie Assistant** 🤖")
    st.write("""
    **Movie Assistant** là chatbot AI thông minh được xây dựng để cung cấp thông tin chi tiết về phim ảnh, bao gồm:
    
    - 🎥 **Tra cứu thông tin phim:** Thông tin chi tiết về phim, diễn viên, thể loại, từ khóa và ngày phát hành.
    - 🍿 **Đề xuất phim hay:** Gợi ý các bộ phim nổi bật dựa trên bộ phim yêu thích của người dùng.
    - 📝 **Phân tích đánh giá:** Hiển thị đánh giá và phản hồi từ khán giả.
    - 🌐 **Truy vấn dữ liệu nâng cao:** Kết nối cơ sở dữ liệu phim ảnh qua truy vấn Cypher và hiển thị kết quả trực quan.
    """)
    st.write("🚀 **Trải nghiệm trò chuyện độc đáo như trong rạp chiếu phim!**")

    st.write("---")
    st.write("📽️ **Version:** 1.0")
    st.write("🍿 **Powered by THMT**")


st.title("🎬 Movie Assistant 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="stChatMessage stChatMessageUser">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="stChatMessage stChatMessageAssistant">{msg["content"]}</div>', unsafe_allow_html=True)

prompt = st.chat_input("🎤 Hãy hỏi về bộ phim bạn yêu thích...")

if prompt:
    st.markdown(
        f'<div class="stChatMessage stChatMessageUser">{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🍿 Đang tìm kiếm thông tin..."):
        reply = chatbot.chat(prompt)

    st.markdown(
        f'<div class="stChatMessage stChatMessageAssistant">{reply}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("""
    <div class="footer">
        🍿 Enjoy your conversation with Movie Assistant | © 2024 Powered by THMT 🚀
    </div>
""", unsafe_allow_html=True)
