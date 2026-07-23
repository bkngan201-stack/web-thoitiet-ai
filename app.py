import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ thống Cảnh báo Thời tiết THPT HCMC", layout="wide", page_icon="🌤️")

# --- KHỞI TẠO TRẠNG THÁI ĐĂNG NHẬP (SESSION STATE) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- CSS TÙY CHỈNH ---
st.markdown("""
    <style>
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f5; }
    .alert-box { padding: 15px; border-radius: 8px; margin-bottom: 15px; font-weight: bold; }
    .sun-alert { background-color: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }
    .rain-alert { background-color: #d1ecf1; color: #0c5460; border-left: 5px solid #17a2b8; }
    .safe-alert { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- CHỨC NĂNG 4: HỆ THỐNG ĐĂNG NHẬP NGƯỜI DÙNG ---
if not st.session_state.logged_in:
    st.title("🔐 Hệ thống Quản lý Sức khỏe Học đường - Đăng nhập")
    st.write("Vui lòng đăng nhập tài khoản học sinh/nhà trường để theo dõi kỹ càng hơn.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        user = st.text_input("Tên đăng nhập (Thử nghiệm: hocsinh)")
        password = st.text_input("Mật khẩu (Thử nghiệm: 123)", type="password")
        
        if st.button("Đăng nhập", type="primary"):
            if user == "hocsinh" and password == "123":
                st.session_state.logged_in = True
                st.session_state.username = user
                st.success("Đăng nhập thành công! Đang tải dữ liệu...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Sai tài khoản hoặc mật khẩu!")
    st.stop() # Dừng chương trình nếu chưa đăng nhập thành công

# --- GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
st.sidebar.title(f"👤 Chào, {st.session_state.username}!")
if st.sidebar.button("Đăng xuất"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🏫 Hệ Thống IoT & AI Quản Trắc Thời Tiết Học Đường TP.HCM")
st.write("Dữ liệu được đồng bộ trực tiếp từ trạm quan trắc cục bộ tại trường THPT.")
st.divider()

# --- CHỨC NĂNG 1: LƯU TRỮ & HIỂN THỊ DỮ LIỆU TỪ TRẠM QUAN TRẮC CỦA BẠN ---
# (Khi làm thật, mục này sẽ đọc file CSV hoặc API Firebase lưu lịch sử trạm đo)
st.header("📊 1. Dữ liệu thực tế từ Trạm Quan Trắc của nhóm")

# Giả lập nhập file dữ liệu từ trạm đo (Các em có thể upload file excel/csv của trạm đo lên đây)
uploaded_file = st.file_uploader("Tải lên tệp dữ liệu trạm đo (.csv) nếu có", type="csv")

if uploaded_file is not None:
    df_iot = pd.read_csv(uploaded_file)
    st.success("Đã đồng bộ dữ liệu trạm đo thành công!")
else:
    # Dữ liệu mẫu lưu trữ của trạm đo để hiển thị
    st.info("💡 Đang hiển thị dữ liệu lưu trữ mặc định của trạm đo IoT tại trường:")
    df_iot = pd.DataFrame({
        'Thời gian': ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
        'Nhiệt độ (°C)': [29.5, 31.0, 33.2, 35.5, 36.8, 36.2, 34.0],
        'Độ ẩm (%)': [85, 80, 75, 70, 65, 68, 72],
        'Chỉ số UV': [2.1, 4.5, 7.0, 9.5, 10.2, 8.8, 5.0]
    })

# Hiển thị các thông số hiện tại (Dòng cuối cùng của trạm đo)
current_data = df_iot.iloc[-1]
c1, c2, c3 = st.columns(3)
with c1: st.metric("Nhiệt độ Trạm đo", f"{current_data['Nhiệt độ (°C)']} °C")
with c2: st.metric("Độ ẩm Trạm đo", f"{current_data['Độ ẩm (%)']} %")
with c3: st.metric("Chỉ số UV Trạm đo", f"{current_data['Chỉ số UV']}")

# Vẽ biểu đồ lịch sử trạm đo
fig_temp = px.line(df_iot, x='Thời gian', y=['Nhiệt độ (°C)', 'Chỉ số UV'], title="Biểu đồ lịch sử trạm đo trong ngày", markers=True)
st.plotly_chart(fig_temp, use_container_width=True)

st.divider()

# --- CHỨC NĂNG 2 & 3: LỜI NHẮC THÔNG MINH & GỬI THÔNG BÁO QUA TIN NHẮN ---
st.header("🔔 2. Trợ lý AI - Nhắc nhở & Gửi thông báo thông minh")

# Lấy thông số hiện tại từ trạm đo để đưa ra lời nhắc tự động
t_hien_tai = current_data['Nhiệt độ (°C)']
uv_hien_tai = current_data['Chỉ số UV']
h_hien_tai = current_data['Độ ẩm (%)']

st.subheader("✉️ Lời nhắc tự động từ hệ thống dành cho bạn:")

loi_nhac_tin_nhan = ""

if t_hien_tai >= 35.0 or uv_hien_tai >= 8.0:
    loi_nhac_tin_nhan = f"[CẢNH BÁO HỌC ĐƯỜNG] Trời đang NẮNG GẮT ({t_hien_tai}°C), UV đạt {uv_hien_tai}. Bạn hãy BÔI KEM CHỐNG NẮNG, mang áo khoác và hạn chế ra sân trường giờ ra chơi nhé!"
    st.markdown(f'<div class="alert-box sun-alert">☀️ {loi_nhac_tin_nhan}</div>', unsafe_allow_html=True)
elif h_hien_tai >= 80.0 and t_hien_tai >= 30.0:
    loi_nhac_tin_nhan = f"[CẢNH BÁO HỌC ĐƯỜNG] Độ ẩm cao ({h_hien_tai}%), nguy cơ CÓ MƯA GIÔNG LỚN. Hãy MANG THEO DÙ/ÁO MƯA khi tan trường và cẩn thận đường trơn trượt!"
    st.markdown(f'<div class="alert-box rain-alert">⛈️ {loi_nhac_tin_nhan}</div>', unsafe_allow_html=True)
else:
    loi_nhac_tin_nhan = "[THÔNG BÁO HỌC ĐƯỜNG] Thời tiết hiện tại rất lý tưởng và an toàn. Chúc các bạn có một ngày học tập thật tốt!"
    st.markdown(f'<div class="alert-box safe-alert">✅ {loi_nhac_tin_nhan}</div>', unsafe_allow_html=True)

# Giao diện gửi SMS / Tin nhắn điện thoại
st.subheader("📱 Tính năng gửi SMS/Tin nhắn nhắc nhở")
sdt = st.text_input("Nhập số điện thoại của bạn hoặc phụ huynh để nhận tin nhắn:", placeholder="090xxxxxxx")

if st.button("📲 Gửi lời nhắc qua tin nhắn ngay lập tức"):
    if sdt:
        with st.spinner("Hệ thống đang kết nối API mạng viễn thông để gửi..."):
            time.sleep(1.5) # Giả lập thời gian gửi qua API tin nhắn
            st.success(f"🎉 Đã gửi tin nhắn SMS thành công đến số {sdt}!")
            st.info(f" Nội dung đã gửi: *\"{loi_nhac_tin_nhan}\"*")
    else:
        st.error("Vui lòng điền số điện thoại trước khi bấm gửi!")
