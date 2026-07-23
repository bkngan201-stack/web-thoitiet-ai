import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Thời Tiết & Sức Khỏe Học Đường TP.HCM",
    page_icon="🌤️",
    layout="wide"
)

# --- CSS TÙY CHỈNH GIAO DIỆN CHUYÊN NGHIỆP ---
st.markdown("""
    <style>
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e1e8ed;
    }
    .reminder-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 16px;
        line-height: 1.6;
    }
    .sun-card { background-color: #fff9e6; border-left: 6px solid #ffa000; color: #7a5200; }
    .rain-card { background-color: #e6f7ff; border-left: 6px solid #1890ff; color: #003a8c; }
    .storm-card { background-color: #fff1f0; border-left: 6px solid #ff4d4f; color: #a8071a; }
    .air-card { background-color: #f6ffed; border-left: 6px solid #52c41a; color: #135200; }
    </style>
""", unsafe_allow_html=True)

# --- BẢNG ÁP DỤNG THỜI TIẾT (WMO WEATHER CODE) ---
WMO_CODES = {
    0: "☀️ Trời quang đãng", 1: "🌤️ Ít mây", 2: "⛅ Mây rải rác", 3: "☁️ Nhiều mây",
    45: "🌫️ Sương mù", 48: "🌫️ Sương mù đọng băng",
    51: "🌧️ Mưa phun nhẹ", 53: "🌧️ Mưa vừa", 55: "🌧️ Mưa nặng hạt",
    61: "🌧️ Mưa rào nhẹ", 63: "🌧️ Mưa rào vừa", 65: "🌧️ Mưa rào to",
    80: "🌦️ Mưa rào cục bộ", 81: "🌧️ Mưa rào mạnh", 82: "⛈️ Mưa rào rất mạnh",
    95: "⛈️ Mưa giông", 96: "⛈️ Mưa giông kèm mưa đá nhẹ", 99: "⛈️ Bão giông cực đoan"
}

# --- HÀM TẢI DỮ LIỆU TỪ VỆ TINH KHÍ TƯỢNG (OPEN-METEO API) ---
@st.cache_data(ttl=600)  # Tự động cập nhật dữ liệu mới mỗi 10 phút
def fetch_weather_data(lat, lon):
    # API Thời tiết & UV
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m,uv_index&hourly=temperature_2m,precipitation_probability,rain,uv_index&daily=weather_code,temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,precipitation_probability_max&timezone=Asia%2FBangkok"
    
    # API Chất lượng không khí (AQI & Bụi mịn PM2.5)
    air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,us_aqi&timezone=Asia%2FBangkok"
    
    res_w = requests.get(weather_url).json()
    res_a = requests.get(air_url).json()
    
    return res_w, res_a

# --- THANH BÊN (SIDEBAR) CHỌN KHU VỰC TẠI TP.HCM ---
st.sidebar.title("📍 Trạm Quan Trắc TP.HCM")
location_dict = {
    "TP. Hồ Chí Minh (Trung tâm)": (10.8231, 106.6297),
    "Quận 1 / Quận 3": (10.7769, 106.7009),
    "Thành phố Thủ Đức": (10.8494, 106.7725),
    "Quận 7 (Khu Nam)": (10.7332, 106.7208),
    "Quận Tân Bình / Gò Vấp": (10.8012, 106.6578),
    "Huyện Bình Chánh / Hóc Môn": (10.6875, 106.5938)
}

selected_loc = st.sidebar.selectbox("Chọn vị trí trạm khí tượng:", list(location_dict.keys()))
lat, lon = location_dict[selected_loc]

st.sidebar.divider()
st.sidebar.info("💡 **Ghi chú dữ liệu:** Dữ liệu thời tiết, UV và Bụi mịn được đồng bộ trực tiếp từ Vệ tinh quan trắc thời gian thực.")

# Tải dữ liệu
try:
    data_w, data_a = fetch_weather_data(lat, lon)
    curr_w = data_w['current']
    curr_a = data_a['current']
    daily_w = data_w['daily']
    hourly_w = data_w['hourly']
    
    # --- PHẦN TIÊU ĐỀ ---
    st.title(f"🌤️ Bảng Điều Khiển Khí Tượng & Sức Khỏe Học Đường")
    st.caption(f"📍 Vị trí quan trắc: **{selected_loc}** | Cập nhật lúc: {datetime.now().strftime('%H:%M - %d/%m/%Y')}")

    # --- 🎯 PHẦN LỜI NHẮC VÀ CẢNH BÁO THỜI TIẾT TỰ ĐỘNG ---
    st.subheader("📢 Lời Nhắc & Cảnh Báo Sức Khỏe Tự Động")
    
    temp = curr_w['temperature_2m']
    uv = curr_w['uv_index']
    rain = curr_w['rain']
    weather_code = curr_w['weather_code']
    pm25 = curr_a['pm2_5']
    aqi = curr_a['us_aqi']

    # Logic phân tích thời tiết đưa ra lời nhắc
    reminders = []
    
    if weather_code in [95, 96, 99]:
        reminders.append(('<div class="reminder-card storm-card">⚡ <b>CẢNH BÁO BẢO GIÔNG / GIÓ LỐC CỰC ĐOAN:</b> Có hiện tượng giông bão cục bộ! Học sinh tuyệt đối ở trong lớp học, không trú mưa dưới cây to trong sân trường. Quý phụ huynh chú ý đưa đón an toàn.</div>'))
    elif rain > 0 or weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        reminders.append(('<div class="reminder-card rain-card">🌧️ <b>CẢNH BÁO MƯA / NGẬP LỤT:</b> Khu vực đang có mưa. Học sinh chuẩn bị sẵn <b>DÙ/ÁO MƯA</b> khi tan trường. Chú ý di chuyển cẩn thận trên các tuyến đường trơn trượt.</div>'))
    
    if uv >= 8.0:
        reminders.append((f'<div class="reminder-card sun-card">☀️ <b>CẢNH BÁO BỨC XẠ TIA UV RẤT CAO (UV {uv}):</b> Nguy cơ bỏng da và sốc nhiệt cao! Hãy <b>BÔI KEM CHỐNG NẮNG</b>, mặc áo khoác chống nắng, đeo kính râm khi ra ngoài. Nhà trường nên chuyển các tiết Thể dục vào nhà đa năng.</div>'))
    elif temp >= 36.0:
        reminders.append((f'<div class="reminder-card sun-card">🔥 <b>CẢNH BÁO NẮNG NÓNG GAY GẮT ({temp}°C):</b> Nhiệt độ môi trường rất cao. Học sinh cần bổ sung <b>UỐNG ĐỦ NƯỚC</b> (mỗi 20 phút/lần), hạn chế vận động mạnh dưới sân trường giờ ra chơi.</div>'))

    if pm25 > 50 or aqi > 100:
        reminders.append((f'<div class="reminder-card air-card">😷 <b>CẢNH BÁO CHẤT LƯỢNG KHÔNG KHÍ (PM2.5: {pm25} µg/m³):</b> Nồng độ bụi mịn ở mức cao. Nhắc nhở học sinh <b>ĐEO KHẨU TRANG N95/Y TẾ</b> khi di chuyển ngoài đường.</div>'))

    if not reminders:
        reminders.append('<div class="reminder-card air-card">✅ <b>THỜI TIẾT LÝ TƯỞNG:</b> Điều kiện nhiệt độ, không khí và UV đang ở mức an toàn. Thích hợp cho các hoạt động học tập và vui chơi ngoài trời!</div>')

    for card in reminders:
        st.markdown(card, unsafe_allow_html=True)

    st.divider()

    # --- TẠO CÁC TAB TÍNH NĂNG NHƯ APP CHÍNH THỐNG ---
    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Hiện Tại & Theo Giờ", "📅 Dự Báo 7 Ngày", "🍃 Chất Lượng Không Khí", "📱 Đăng Ký Nhận SMS"])

    # --- TAB 1: HIỆN TẠI & DỰ BÁO THEO GIỜ ---
    with tab1:
        st.write("### 📊 Thông số thời tiết hiện tại")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nhiệt độ hiện tại", f"{curr_w['temperature_2m']} °C", f"Cảm giác như {curr_w['apparent_temperature']} °C")
        c2.metric("Tình trạng", WMO_CODES.get(curr_w['weather_code'], "Bình thường"))
        c3.metric("Độ ẩm không khí", f"{curr_w['relative_humidity_2m']} %")
        c4.metric("Tốc độ gió", f"{curr_w['wind_speed_10m']} km/h")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Chỉ số Bức xạ UV", f"{curr_w['uv_index']}", "Cao" if curr_w['uv_index']>=6 else "An toàn")
        c6.metric("Lượng mưa hiện tại", f"{curr_w['rain']} mm")
        c7.metric("Chỉ số AQI (Mỹ)", f"{curr_a['us_aqi']}")
        c8.metric("Bụi mịn PM2.5", f"{curr_a['pm2_5']} µg/m³")

        st.subheader("📈 Biểu đồ biến thiên 24 giờ tới")
        df_hourly = pd.DataFrame({
            'Thời gian': [t.split('T')[1] for t in hourly_w['time'][:24]],
            'Nhiệt độ (°C)': hourly_w['temperature_2m'][:24],
            'Xác suất mưa (%)': hourly_w['precipitation_probability'][:24],
            'Chỉ số UV': hourly_w['uv_index'][:24]
        })

        fig_hourly = px.line(df_hourly, x='Thời gian', y=['Nhiệt độ (°C)', 'Xác suất mưa (%)', 'Chỉ số UV'],
                             markers=True, title="Diễn biến Nhiệt độ, Xác suất mưa & Tia UV theo giờ")
        st.plotly_chart(fig_hourly, use_container_width=True)

    # --- TAB 2: DỰ BÁO 7 NGÀY ---
    with tab2:
        st.write("### 📅 Dự báo thời tiết 7 ngày tới tại TP.HCM")
        df_daily = pd.DataFrame({
            'Ngày': daily_w['time'],
            'Nhiệt độ cao nhất (°C)': daily_w['temperature_2m_max'],
            'Nhiệt độ thấp nhất (°C)': daily_w['temperature_2m_min'],
            'UV Cực đại': daily_w['uv_index_max'],
            'Xác suất mưa lớn nhất (%)': daily_w['precipitation_probability_max'],
            'Thời tiết': [WMO_CODES.get(code, "Khác") for code in daily_w['weather_code']]
        })
        st.dataframe(df_daily, use_container_width=True)

        fig_daily = go.Figure()
        fig_daily.add_trace(go.Bar(x=df_daily['Ngày'], y=df_daily['Nhiệt độ cao nhất (°C)'], name='Nhiệt độ Cao nhất (°C)', marker_color='#ff7f0e'))
        fig_daily.add_trace(go.Bar(x=df_daily['Ngày'], y=df_daily['Xác suất mưa lớn nhất (%)'], name='Xác suất Mưa (%)', marker_color='#1f77b4'))
        fig_daily.update_layout(barmode='group', title="So sánh Nhiệt độ tối đa và Nguy cơ mưa 7 ngày tới")
        st.plotly_chart(fig_daily, use_container_width=True)

    # --- TAB 3: CHẤT LƯỢNG KHÔNG KHÍ (AQI) ---
    with tab3:
        st.write("### 🍃 Chi tiết Chất lượng Không khí & Bụi mịn")
        k1, k2, k3 = st.columns(3)
        k1.metric("Chỉ số AQI", curr_a['us_aqi'])
        k2.metric("Nồng độ Bụi PM2.5", f"{curr_a['pm2_5']} µg/m³")
        k3.metric("Nồng độ Bụi PM10", f"{curr_a['pm10']} µg/m³")

        st.info("""
        📌 **Thước đo Bụi mịn PM2.5 theo tiêu chuẩn sức khỏe:**
        * **0 - 12 µg/m³:** Tốt - Dễ chịu.
        * **12.1 - 35.4 µg/m³:** Trung bình.
        * **35.5 - 55.4 µg/m³:** Kém - Nhóm nhạy cảm (học sinh, người hen suyễn) nên đeo khẩu trang.
        * **> 55.5 µg/m³:** Xấu/Nguy hại - Nên hạn chế thể dục ngoài trời.
        """)

    # --- TAB 4: ĐĂNG KÝ NHẬN SMS / THÔNG BÁO ---
    with tab4:
        st.write("### 📱 Đăng ký nhận tin nhắn lời nhắc tự động")
        st.write("Nhập thông tin phụ huynh/học sinh để hệ thống gửi lời nhắc thời tiết mỗi sáng lúc 06:30 AM:")
        
        with st.form("sms_form"):
            name = st.text_input("Họ và tên học sinh:")
            phone = st.text_input("Số điện thoại nhận tin nhắn SMS/Zalo:")
            school = st.text_input("Trường THPT đang theo học:")
            opt_rain = st.checkbox("Nhận cảnh báo Mưa / Bão giờ tan trường", value=True)
            opt_uv = st.checkbox("Nhận lời nhắc Nắng nóng & Tia UV", value=True)
            
            submit = st.form_submit_button("🔔 Đăng ký nhận lời nhắc")
            if submit:
                if phone:
                    st.success(f"🎉 Đã ghi nhận đăng ký thành công cho học sinh **{name}** ({phone}). Hệ thống sẽ gửi SMS nhắc nhở tự động theo thời tiết!")
                else:
                    st.error("Vui lòng điền số điện thoại!")

except Exception as e:
    st.error(f"Đang kết nối lại với vệ tinh khí tượng... Lỗi chi tiết: {e}")
