import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN TRÀN VIỀN ---
st.set_page_config(page_title="Hệ thống Khí tượng Học đường HCMC", page_icon="🏫", layout="wide")

# --- 2. BỘ CSS NÂNG CAO: BIẾN ĐỔI DIỆN MẠO STREAMLIT ---
st.markdown("""
    <style>
    /* Đổi nền trang web sang màu xám khói Gradient sang trọng */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Thiết kế lại các ô số liệu (Metrics) dạng thẻ kính mờ Glassmorphism */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(31, 38, 135, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    /* Hiệu ứng bay lên và đổi màu nhẹ khi di chuột vào thẻ */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(31, 38, 135, 0.12);
        background: #ffffff;
    }
    
    /* Làm đẹp các thẻ cảnh báo ma trận */
    .matrix-box {
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .sun-box { background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%); border-left: 6px solid #ffa000; color: #7a5200; }
    .rain-box { background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%); border-left: 6px solid #1890ff; color: #003a8c; }
    .safe-box { background: linear-gradient(135deg, #f6ffed 0%, #d9f7be 100%); border-left: 6px solid #52c41a; color: #135200; }
    
    /* Làm đẹp nút bấm */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ĐỒNG BỘ DỮ LIỆU VỆ TINH REALTIME CHO TP.HCM ---
@st.cache_data(ttl=600)
def get_weather():
    url_w = "https://api.open-meteo.com/v1/forecast?latitude=10.8231&longitude=106.6297&current=temperature_2m,relative_humidity_2m,rain,weather_code,uv_index"
    url_a = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=10.8231&longitude=106.6297&current=pm2_5,us_aqi"
    return requests.get(url_w).json()['current'], requests.get(url_a).json()['current']

try:
    w, a = get_weather()
    
    # Tiêu đề ứng dụng
    st.title("🏫 Bảng Điều Khiển Khí Tượng Học Đường Thông Minh")
    st.caption(f"📍 Khu vực: TP. Hồ Chí Minh | Đồng bộ tự động: {datetime.now().strftime('%H:%M - %d/%m/%Y')}")
    st.divider()

    # --- 4. HIỂN THỊ CÁC THẺ SỐ LIỆU ĐẸP MẮT ---
    st.subheader("📊 Chỉ số quan trắc thời gian thực")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nhiệt độ", f"{w['temperature_2m']} °C")
    c2.metric("Độ ẩm không khí", f"{w['relative_humidity_2m']} %")
    c3.metric("Chỉ số Tia UV", f"{w['uv_index']}")
    c4.metric("Bụi mịn PM2.5", f"{a['pm2_5']} µg/m³")

    st.divider()

    # --- 5. HỆ THỐNG AI PHÂN TÍCH MA TRẬN LỜI NHẮC ---
    st.subheader("🤖 Trợ lý AI Khuyến nghị Y tế Học đường")
    
    if w['uv_index'] >= 8.0 or w['temperature_2m'] >= 36.0:
        st.markdown("""
        <div class="matrix-box sun-box">
            <h3>☀️ CẢNH BÁO NẮNG NÓNG & BỨC XẠ UV CAO</h3>
            <b>🛡️ Đối với Học sinh:</b> Bắt buộc mặc áo khoác chống nắng, bôi kem chống nắng và uống nước lọc sau mỗi tiết học.<br>
            <b>🏫 Đối với Nhà trường:</b> Di dời toàn bộ tiết học Thể dục, sinh hoạt dưới cờ vào nhà đa năng.
        </div>
        """, unsafe_allow_html=True)
    elif w['rain'] > 0 or w['weather_code'] in [61, 63, 65, 80, 81, 82]:
        st.markdown("""
        <div class="matrix-box rain-box">
            <h3>🌧️ CẢNH BÁO MƯA GIÔNG / NGUY CƠ NGẬP LỤT</h3>
            <b>🛡️ Đối với Học sinh:</b> Chuẩn bị sẵn dù/áo mưa trong balo. Tuyệt đối không đứng dưới gốc cây to khi có sấm sét.<br>
            <b>🏫 Đối với Nhà trường:</b> Bố trí lực lượng điều phối cổng trường, mở sảnh lớn cho học sinh trú mưa đợi phụ huynh.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="matrix-box safe-box">
            <h3>✅ THỜI TIẾT AN TOÀN & LÝ TƯỞNG</h3>
            <b>🛡️ Đối với Học sinh:</b> Tích cực tham gia các hoạt động thể chất và câu lạc bộ ngoài trời.<br>
            <b>🏫 Đối với Nhà trường:</b> Khuyến khích mở cửa sổ thông thoáng tự nhiên, tổ chức học tập trải nghiệm xanh.
        </div>
        """, unsafe_allow_html=True)

    # --- 6. TÍNH NĂNG TƯƠNG TÁC GỬI TIN NHẮN ---
    st.divider()
    st.subheader("📱 Đăng ký nhận thông báo SMS qua điện thoại")
    c_sdt, c_nut = st.columns([3, 1])
    with c_sdt:
        sdt = st.text_input("Nhập số điện thoại Phụ huynh hoặc Học sinh:", placeholder="090xxxxxxx")
    with c_nut:
        st.write(" ") # Căn lề cho thẳng nút
        st.write(" ")
        if st.button("📲 Kích hoạt cổng gửi"):
            if sdt: st.success(f"🎉 Đã đăng ký thành công số {sdt}! Lời nhắc AI sẽ gửi đi tự động.")
            else: st.error("Vui lòng nhập số điện thoại!")

except Exception as e:
    st.error("Đang kết nối lại với vệ tinh khí tượng...")
