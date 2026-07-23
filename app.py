import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Weather & Health HCMC", layout="wide", page_icon="🏫")

# --- CSS TÙY CHỈNH ĐỂ GIAO DIỆN ĐẸP HƠN ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .health-card { background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #03a9f4; }
    </style>
    """, unsafe_content_id=True)

# --- THANH BÊN (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4052/4052984.png", width=100)
st.sidebar.title("Hệ thống IoT - AI")
st.sidebar.info("Dự án: Dự báo thời tiết cực đoan & Bảo vệ sức khỏe học sinh THPT TP.HCM")

# --- TẠO CÁC TAB CHỨC NĂNG ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard IoT", "🤖 Dự báo AI", "🏥 Giải pháp Sức khỏe", "📅 Lịch sử dữ liệu"])

with tab1:
    st.title("🏠 Bảng điều khiển quan trắc thời gian thực")
    st.write(f"Cập nhật mới nhất: {datetime.now().strftime('%H:%M:%S')} - Khu vực: TP. Hồ Chí Minh")
    
    # Giả lập dữ liệu từ trạm IoT ESP32
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Nhiệt độ", "34.5°C", "1.2°C")
    with col2: st.metric("Độ ẩm", "78%", "-3%")
    with col3: st.metric("Chỉ số UV", "9.2", "Nguy hiểm", delta_color="inverse")
    with col4: st.metric("Bụi PM2.5", "42 µg/m³", "Khá")

    # Vẽ biểu đồ Plotly tương tác
    df_sim = pd.DataFrame({
        'Giờ': list(range(8, 18)),
        'Nhiệt độ': [28, 29, 31, 33, 35, 34.5, 33, 31, 30, 29],
        'UV': [2, 4, 6, 8, 10, 9.2, 7, 4, 2, 1]
    })
    fig = px.line(df_sim, x='Giờ', y=['Nhiệt độ', 'UV'], title="Biến thiên thông số trong ngày", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.title("🤖 Trung tâm Dự báo thời tiết cực đoan bằng AI")
    st.write("Nhập dữ liệu giả định để AI phân tích nguy cơ thiên tai cục bộ")
    
    c1, c2 = st.columns(2)
    with c1:
        temp_input = st.slider("Nhiệt độ dự báo (°C)", 20, 45, 35)
        uv_input = st.slider("Chỉ số UV dự báo", 0, 12, 9)
    with c2:
        rain_prob = st.slider("Xác suất mưa (%)", 0, 100, 85)
        wind_speed = st.slider("Tốc độ gió (km/h)", 0, 100, 20)

    if st.button("🚀 Kích hoạt AI dự báo nguy cơ"):
        with st.spinner("Đang chạy mô hình AI..."):
            # Logic AI giả định (Các em có thể thay bằng model thật)
            if temp_input > 37 or uv_input > 9:
                st.error("🚨 CẢNH BÁO: Nắng nóng cực đoan & Bức xạ UV độc hại mức tím!")
                st.warning("Nguy cơ: Sốc nhiệt, bỏng da, mất nước diện rộng tại các trường học.")
            elif rain_prob > 80 and wind_speed > 40:
                st.warning("⛈️ CẢNH BÁO: Nguy cơ Giông lốc cục bộ & Ngập lụt giờ tan trường!")
                st.info("Khu vực chú ý: Các quận thấp trũng (Q.7, Q.Bình Thạnh, TP.Thủ Đức).")
            else:
                st.success("✅ Dự báo: Thời tiết ổn định, phù hợp hoạt động giáo dục.")

with tab3:
    st.title("🏥 Giải pháp & Khuyến nghị Sức khỏe")
    st.write("Đề xuất dành riêng cho học sinh THPT tại địa bàn TP.HCM")
    
    st.markdown("""
    <div class="health-card">
        <h3>1. Đối với học sinh:</h3>
        <ul>
            <li><b>Di chuyển:</b> Đeo khẩu trang N95, mặc áo khoác chống UV khi tan trường.</li>
            <li><b>Dinh dưỡng:</b> Uống ít nhất 500ml nước xen kẽ giữa các tiết học. Bổ sung nước điện giải nếu có tiết Thể dục.</li>
            <li><b>Phòng ngừa:</b> Không đứng dưới cây xanh lớn khi có mây đen kéo tới (đề phòng lốc xoáy cục bộ).</li>
        </ul>
    </div>
    <br>
    <div class="health-card" style="border-left-color: #4caf50; background-color: #e8f5e9;">
        <h3>2. Đối với nhà trường (Ban Giám Hiệu):</h3>
        <ul>
            <li><b>Điều chỉnh:</b> Chuyển tiết Chào cờ hoặc Thể dục vào nhà đa năng nếu UV > 8 hoặc Nhiệt độ > 36°C.</li>
            <li><b>Cơ sở vật chất:</b> Kiểm tra hệ thống thoát nước quanh cổng trường để tránh kẹt xe/ngập lụt giờ tan tầm.</li>
        </ul>
    </div>
    """, unsafe_content_id=True)

with tab4:
    st.title("📅 Lịch sử quan trắc hệ thống")
    data_logs = pd.DataFrame({
        'Ngày': ['2024-05-20', '2024-05-21', '2024-05-22'],
        'Hiện tượng': ['Nắng gắt', 'Mưa giông Q.1', 'Nắng nóng'],
        'Mức độ': ['Cao', 'Nguy hiểm', 'Trung bình'],
        'AI Dự báo': ['Chính xác', 'Chính xác', 'Sai lệch thấp']
    })
    st.table(data_logs)
