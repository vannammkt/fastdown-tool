import streamlit as st
import yt_dlp
import os
import tempfile
import time

# -----------------------------------------------------------------------------
# CẤU HÌNH TRANG (PAGE CONFIG)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FastDown - Tải Video Nhanh",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS & BRANDING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Tổng quan nền tối */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Ẩn Main Menu & Footer mặc định */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Style cho Tiêu đề */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        color: #ffffff;
    }
    .sub-title {
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        color: #d32123; /* Đỏ thương hiệu */
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Style cho Ô nhập liệu (Input) */
    div[data-baseweb="input"] {
        border-radius: 10px;
        background-color: #1c1f26;
        border: 1px solid #333;
    }
    /* Hiệu ứng Glow khi focus */
    div[data-baseweb="input"]:focus-within {
        border: 1px solid #d32123;
        box-shadow: 0 0 15px rgba(211, 33, 35, 0.4);
    }
    input.stTextInput {
        color: white;
    }

    /* Style cho Nút bấm chính (Button & Download Button) */
    div.stButton > button:first-child, 
    div.stDownloadButton > button:first-child {
        background-color: #d32123;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 2rem;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-color: #ff4d4d;
        box-shadow: 0 6px 12px rgba(211, 33, 35, 0.4);
        transform: translateY(-2px);
        color: white;
        border-color: #ff4d4d;
    }

    /* Style cho Popular Tool Card */
    .tool-card {
        background-color: #1c1f26;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: transform 0.2s;
        margin-bottom: 10px;
    }
    .tool-card:hover {
        border-color: #d32123;
        transform: scale(1.03);
    }
    .tool-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }
    .tool-name {
        font-weight: bold;
        font-size: 14px;
        color: #fff;
        margin-bottom: 5px;
    }
    .tool-desc {
        font-size: 11px;
        color: #aaa;
    }
    
    /* Social Icons Row */
    .social-row {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 40px;
        font-size: 24px;
        letter-spacing: 20px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HEADER & INPUT SECTION
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">Tải Video Từ Mọi Nền Tảng</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Nhanh & Miễn Phí</div>', unsafe_allow_html=True)

# Form nhập liệu
url_input = st.text_input("", placeholder="Dán link YouTube, Facebook, TikTok vào đây...", label_visibility="collapsed")

# Nút Action
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    start_download = st.button("TẢI NGAY")

# Social Icons
st.markdown("""
<div class="social-row">
    <span>📺</span> <span>📘</span> <span>🎵</span> <span>✖️</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LOGIC XỬ LÝ DOWNLOAD (BACKEND)
# -----------------------------------------------------------------------------
if start_download and url_input:
    if not url_input.strip():
        st.error("⚠️ Vui lòng nhập đường dẫn video!")
    else:
        status_placeholder = st.empty()
        
        try:
            with status_placeholder.container():
                with st.spinner('Đang phân tích và tải video... Vui lòng chờ...'):
                    # Tạo thư mục tạm an toàn
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Cấu hình yt-dlp
                        ydl_opts = {
                            'format': 'best[ext=mp4]/best', # Ưu tiên MP4 tốt nhất
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                            'quiet': True,
                            'no_warnings': True,
                            'noplaylist': True,
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            # Lấy thông tin trước
                            info_dict = ydl.extract_info(url_input, download=True)
                            
                            video_title = info_dict.get('title', 'video')
                            thumbnail_url = info_dict.get('thumbnail', None)
                            
                            # Tìm file đã tải về trong thư mục tạm
                            downloaded_file_path = ydl.prepare_filename(info_dict)
                            
                            # Xử lý trường hợp yt-dlp đổi đuôi file (ví dụ merge video+audio)
                            if not os.path.exists(downloaded_file_path):
                                # Quét file trong thư mục tạm nếu tên không khớp chính xác
                                files = os.listdir(temp_dir)
                                if files:
                                    downloaded_file_path = os.path.join(temp_dir, files[0])

                            # Đọc file vào RAM để download và xóa file tạm ngay
                            with open(downloaded_file_path, "rb") as f:
                                file_data = f.read()
            
            # Xóa UI loading
            status_placeholder.empty()

            # HIỂN THỊ KẾT QUẢ
            st.success("✅ Đã xử lý xong video!")
            
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                if thumbnail_url:
                    st.image(thumbnail_url, use_column_width=True)
                else:
                    st.info("Không có ảnh bìa.")
            
            with res_col2:
                st.markdown(f"**Tiêu đề:** {video_title}")
                st.markdown("---")
                # Nút tải file về máy
                st.download_button(
                    label="Tải Video MP4 Về Máy",
                    data=file_data,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4"
                )
                
        except Exception as e:
            status_placeholder.empty()
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
            st.warning("Vui lòng kiểm tra lại đường dẫn hoặc thử link khác.")

elif start_download and not url_input:
    st.error("⚠️ Bạn chưa nhập liên kết video!")

# -----------------------------------------------------------------------------
# POPULAR TOOLS SECTION
# -----------------------------------------------------------------------------
st.markdown("### Popular Tools")

tools_data = [
    {"icon": "🎵", "name": "YouTube sang MP3", "desc": "Chuyển đổi video YouTube sang MP3 chất lượng cao."},
    {"icon": "📺", "name": "Trình tải YouTube", "desc": "Tải xuống video YouTube định dạng HD."},
    {"icon": "📸", "name": "Tải Instagram", "desc": "Lưu video, Reels, Stories từ Instagram."},
    {"icon": "📘", "name": "Tải Facebook", "desc": "Tải video Facebook chất lượng cao nhất."},
    {"icon": "🎵", "name": "Tải TikTok", "desc": "Tải video TikTok không dính logo (Watermark)."},
    {"icon": "✖️", "name": "Tải Twitter (X)", "desc": "Lưu video và GIF từ mạng xã hội X."},
    {"icon": "📌", "name": "Tải Pinterest", "desc": "Tải video và ảnh từ Pinterest nhanh chóng."},
    {"icon": "🤖", "name": "Tải Reddit", "desc": "Tải video Reddit có kèm âm thanh."},
]

# Chia thành 2 hàng, mỗi hàng 4 cột
rows = [tools_data[i:i + 4] for i in range(0, len(tools_data), 4)]

for row_items in rows:
    cols = st.columns(4)
    for idx, tool in enumerate(row_items):
        with cols[idx]:
            # Render Card HTML
            st.markdown(f"""
            <div class="tool-card">
                <div class="tool-icon">{tool['icon']}</div>
                <div class="tool-name">{tool['name']}</div>
                <div class="tool-desc">{tool['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
