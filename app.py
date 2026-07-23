import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Hệ thống Dự báo Thời tiết Cực đoan THPT TP.HCM",
    page_icon="⛈️",
    layout="wide"
)

# Tiêu đề chính
st.title("⛈️ Hệ thống IoT & AI Dự báo Thời tiết Cực đoan Cục bộ")
st.markdown("### *Đề tài đề xuất giải pháp bảo vệ sức khỏe cho học sinh THPT tại địa bàn TP.Hồ Chí Minh*")
st.divider()

# ==========================================
# 2. GIẢ LẬP DỮ LIỆU TỪ TRẠM IOT (ĐỂ DEMO)
# ==========================================
# Khi làm thật, các em sẽ viết code đọc dữ liệu từ Firebase/Google Sheets ở đây.
@st.cache_data
def load_iot_history():
    # Tạo 24 giờ dữ liệu giả lập cho trạm đo tại trường THPT
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    data = {
        "Thời gian": times,
        "Nhiệt độ (°C)": [round(random.uniform(26.0, 36.5), 1) for _ in range(24)],
        "Độ ẩm (%)": [round(random.uniform(60.0, 95.0), 1) for _ in range(24)],
        "Chỉ số UV": [round(random.uniform(1.0, 11.5), 1) for _ in range(24)],
        "Bụi mịn PM2.5 (µg/m³)": [round(random.uniform(15.0, 65.0), 1) for _ in range(24)]
    }
    return pd.DataFrame(data)

df_iot = load_iot_history()
latest_data = df_iot.iloc[-1] # Lấy dòng dữ liệu mới nhất

# ==========================================
# 3. HIỂN THỊ DỮ LIỆU THỜI GIAN THỰC (METRICS)
# ==========================================
st.header("📊 Dữ liệu thời gian thực từ Trạm đo IoT")
st.caption("Vị trí trạm: Khuôn viên trường THPT tại TP.HCM - Cập nhật tự động")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="🌡️ Nhiệt độ hiện tại", value=f"{latest_data['Nhiệt độ (°C)']} °C", delta="Mùa nắng gắt")
with col2:
    st.metric(label="💧 Độ ẩm không khí", value=f"{latest_data['Độ ẩm (%)']} %", delta="Độ ẩm cao")
with col3:
    st.metric(label="☀️ Chỉ số tia UV", value=latest_data['Chỉ số UV'], delta="Cảnh báo bức xạ", delta_color="inverse")
with col4:
    st.metric(label="😷 Bụi mịn PM2.5", value=f"{latest_data['Bụi mịn PM2.5 (µg/m³)' ]} µg/m³", delta="Chỉ số AQI")

st.divider()

# ==========================================
# 4. THIẾT KẾ GIAO DIỆN CHÍNH (CHIA LÀM 2 TAB)
# ==========================================
tab_graphs, tab_ai = st.tabs(["📈 Biểu đồ xu hướng IoT", "🤖 Trí tuệ nhân tạo (AI) Dự báo & Khuyến nghị"])

# --- TAB 1: BIỂU ĐỒ XU HƯỚNG ---
with tab_graphs:
    st.subheader("Đồ thị theo dõi diễn biến thời tiết trong ngày")
    
    # Chọn thông số để vẽ biểu đồ
    option = st.selectbox(
        'Chọn thông số muốn xem xu hướng:',
        ('Nhiệt độ (°C)', 'Độ ẩm (%)', 'Chỉ số UV', 'Bụi mịn PM2.5 (µg/m³)'))
    
    fig = px.line(df_iot, x='Thời gian', y=option, title=f'Xu hướng thay đổi {option} trong 24 giờ qua')
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AI DỰ BÁO VÀ GIẢI PHÁP ---
with tab_ai:
    st.subheader("Mô phỏng Mô hình AI Dự báo Thời tiết Cực đoan cục bộ")
    st.write("Nhập thông số thời tiết cục bộ dưới đây để mô hình AI phân tích đưa ra cảnh báo sớm trong 1-2 giờ tới:")

    # Tạo các thanh trượt nhập dữ liệu đầu vào cho AI
    c1, c2 = st.columns(2)
    with c1:
        input_temp = st.slider("Dự báo Nhiệt độ môi trường (°C)", 20.0, 45.0, float(latest_data['Nhiệt độ (°C)']))
        input_humidity = st.slider("Dự báo Độ ẩm không khí (%)", 30, 100, int(latest_data['Độ ẩm (%)']))
    with c2:
        input_uv = st.slider("Dự báo Chỉ số UV cao nhất", 0.0, 15.0, float(latest_data['Chỉ số UV']))
        input_pm25 = st.slider("Dự báo Nồng độ bụi mịn PM2.5 (µg/m³)", 0, 150, int(latest_data['Bụi mịn PM2.5 (µg/m³)']))

    # Nút bấm kích hoạt AI
    if st.button("KÍCH HOẠT AI PHÂN TÍCH DỰ BÁO"):
        with st.spinner('AI đang tính toán dữ liệu cục bộ...'):
            # Giả lập thời gian AI xử lý (0.5 giây)
            import time
            time.sleep(0.5)
            
            # ----------------------------------------------------------------
            # LOGIC AI GIẢ LẬP (Khi làm thật, các em sẽ load model .pkl tại đây)
            # ----------------------------------------------------------------
            status = "Bình thường"
            recommendation = ""
            
            if input_temp >= 37.0 or input_uv >= 9.0:
                status = "Nguy cơ Nắng nóng cực đoan / Sốc nhiệt"
                recommendation = """
                **Khuyến nghị bảo vệ sức khỏe cho học sinh:**
                1. Nhà trường hạn chế cho học sinh chào cờ hoặc sinh hoạt ngoại khóa ngoài trời vào khung giờ từ 10h00 - 15h00.
                2. Học sinh cần uống đủ nước (bổ sung nước khoáng), mặc áo khoác chống nắng, bôi kem chống nắng và đeo kính râm khi đến trường.
                3. Bật hệ thống phun sương làm mát hoặc điều hòa tại các lớp học.
                """
                st.error(f"🚨 **CẢNH BÁO TỪ AI:** {status}")
                
            elif input_humidity >= 85.0 and input_temp >= 32.0:
                status = "Nguy cơ Mưa dông kèm lốc xoáy / Ngập lụt cục bộ tại TP.HCM"
                recommendation = """
                **Khuyến nghị bảo vệ sức khỏe và an toàn:**
                1. Nhắc nhở học sinh mang theo áo mưa cá nhân khi đi học.
                2. Trong giờ tan trường nếu có mưa lớn, học sinh tuyệt đối không đứng trú mưa dưới gốc cây cổ thụ hoặc gần cột điện.
                3. Phụ huynh và học sinh chủ động lộ trình di chuyển tránh các tuyến đường hay ngập nặng tại TP.HCM (như Nguyễn Văn Quá, Quốc Hương, Kha Vạn Cân...).
                """
                st.warning(f"⚠️ **CẢNH BÁO TỪ AI:** {status}")
                
            elif input_pm25 >= 50.0:
                status = "Ô nhiễm không khí cục bộ (Chỉ số bụi mịn PM2.5 tăng cao)"
                recommendation = """
                **Khuyến nghị bảo vệ đường hô hấp:**
                1. Học sinh bắt buộc đeo khẩu trang y tế chuẩn N95 hoặc khẩu trang vải dày khi di chuyển bằng xe máy/xe đạp đến trường.
                2. Giảm các hoạt động thể dục thể thao ngoài trời, đóng bớt các cửa sổ lớp học hướng ra mặt đường lớn.
                """
                st.info(f"😷 **CẢNH BÁO TỪ AI:** {status}")
                
            else:
                status = "Thời tiết An toàn - Ổn định"
                recommendation = """
                **Khuyến nghị:**
                - Thời tiết lý tưởng cho mọi hoạt động học tập, thể thao ngoài trời của học sinh. Tiếp tục duy trì theo dõi hệ thống.
                """
                st.success(f"✅ **KẾT QUẢ TỪ AI:** {status}")
            
            # Hiển thị giải pháp sức khỏe cụ thể
            st.markdown("### 📋 ĐỀ XUẤT GIẢI PHÁP BẢO VỆ SỨC KHỎE:")
            st.write(recommendation)

# ==========================================
# 5. PHẦN CHÂN TRANG (FOOTER)
# ==========================================
st.divider()
st.centered = st.markdown("<center><small>Bản quyền nghiên cứu khoa học © 2026 - Nhóm nghiên cứu THPT TP.HCM</small></center>", unsafe_allow_html=True)
