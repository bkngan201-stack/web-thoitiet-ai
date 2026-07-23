import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Weather HCMC", page_icon="🏫", layout="wide")

# CSS Tùy chỉnh (Đã sửa chuẩn cú pháp để không bị lỗi)
st.markdown("""
    <style>
    .stMetric { background-color: #f0f8ff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .health-box { background-color: #e8f5e9; padding: 20px; border-left: 5px solid #4caf50; border-radius: 5px; margin-bottom: 15px; }
    .danger-box { background-color: #ffebee; padding: 20px; border-left: 5px solid #f44336; border-radius: 5px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- TIÊU ĐỀ DỰ ÁN ---
st.title("⛈️ Hệ Thống IoT & AI Dự Báo Thời Tiết Cực Đoan Cục Bộ")
st.markdown("**Mục tiêu:** Đề xuất giải pháp bảo vệ sức khỏe cho học sinh THPT tại địa bàn TP.HCM")
st.divider()

# --- TẠO CÁC TAB CHỨC NĂNG ---
tab1, tab2, tab3 = st.tabs(["📊 Trạm Quan Trắc IoT", "🤖 AI Dự Báo & Cảnh Báo", "🏥 Sổ Tay Sức Khỏe"])

# --- TAB 1: DỮ LIỆU IOT THỜI GIAN THỰC ---
with tab1:
    st.header("Thông số môi trường hiện tại")
    
    # Giả lập dữ liệu thời gian thực
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="Nhiệt độ", value="35.2 °C", delta="+1.2 °C")
    with col2: st.metric(label="Độ ẩm", value="75 %", delta="-2 %")
    with col3: st.metric(label="Chỉ số UV", value="8.5", delta="Cao", delta_color="inverse")
    with col4: st.metric(label="Bụi mịn PM2.5", value="45 µg/m³", delta="Trung bình")
    
    st.subheader("Biến thiên nhiệt độ trong 12 giờ qua")
    # Biểu đồ Plotly chuyên nghiệp
    df_chart = pd.DataFrame({
        'Thời gian (Giờ)': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'Nhiệt độ (°C)': [27, 29, 31, 33, 35, 36, 35.2, 34, 32, 30]
    })
    fig = px.line(df_chart, x='Thời gian (Giờ)', y='Nhiệt độ (°C)', markers=True, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: MÔ HÌNH AI DỰ BÁO ---
with tab2:
    st.header("Kiểm thử Mô hình Trí tuệ nhân tạo")
    st.write("Nhập các thông số dự kiến để AI phân tích và đưa ra cảnh báo.")
    
    c1, c2 = st.columns(2)
    with c1:
        nhap_nhietdo = st.slider("Nhiệt độ (°C)", 20.0, 45.0, 36.5)
        nhap_uv = st.slider("Chỉ số UV", 0.0, 12.0, 9.0)
    with c2:
        nhap_doam = st.slider("Độ ẩm (%)", 30.0, 100.0, 85.0)
        
    if st.button("🚀 Kích hoạt AI Phân tích", type="primary"):
        st.divider()
        if nhap_nhietdo >= 37.0 or nhap_uv >= 9.0:
            st.error("🚨 CẢNH BÁO MỨC ĐỘ NGUY HIỂM: Nắng nóng cực đoan & Tia UV bức xạ cao!")
            st.markdown("""
                <div class="danger-box">
                    <b>Khuyến nghị khẩn cấp:</b><br>
                    - Tạm dừng toàn bộ các tiết học Thể dục ngoài trời.<br>
                    - Không tổ chức sinh hoạt dưới cờ ở sân trường không có mái che.<br>
                    - Nhắc nhở học sinh có tiền sử tim mạch, huyết áp hạn chế di chuyển.
                </div>
                """, unsafe_allow_html=True)
        elif nhap_doam >= 85.0 and nhap_nhietdo >= 32.0:
            st.warning("⚠️ CẢNH BÁO MỨC ĐỘ TRUNG BÌNH: Nguy cơ mưa giông & Ngập lụt cục bộ.")
            st.markdown("""
                <div class="health-box">
                    <b>Khuyến nghị phòng ngừa:</b><br>
                    - Học sinh chuẩn bị sẵn áo mưa khi tan trường.<br>
                    - Tránh trú mưa dưới các gốc cây cổ thụ lớn trong khuôn viên trường.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ THỜI TIẾT ỔN ĐỊNH: Chỉ số an toàn cho các hoạt động giáo dục.")

# --- TAB 3: GIẢI PHÁP SỨC KHỎE ---
with tab3:
    st.header("Cẩm nang bảo vệ sức khỏe học đường")
    st.write("Dựa trên phân tích dữ liệu khí hậu đặc thù của TP.HCM, hệ thống đề xuất:")
    
    st.markdown("""
    * **Quản lý nước uống:** Học sinh cần bổ sung 1.5 - 2 lít nước mỗi ngày, ưu tiên uống nước lọc xen kẽ các tiết học, đặc biệt vào những ngày nắng nóng (tháng 3 - tháng 5).
    * **Trang bị cá nhân:** Sử dụng kem chống nắng, áo khoác dày dặn và kính râm khi di chuyển trên các tuyến đường ít bóng râm.
    * **Giải pháp từ nhà trường:** Cần bố trí thêm hệ thống quạt thông gió tại các hành lang và hệ thống mái che cơ động ở khu vực căn tin.
    """)
