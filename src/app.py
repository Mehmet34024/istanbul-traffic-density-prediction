import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# 1. v0 TEMA VE SAYFA YAPILANDIRMASI:
st.set_page_config(
    page_title="Trafik-Sens Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Geist', sans-serif !important;
    }
    
    .stApp {
        background-color: #f8fafc !important; 
    }
    
    [data-testid="stMainBlockContainer"] {
        max-width: 95% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 2rem !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* v0 Modern Kart Yapısı */
    .v0-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 0.625rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
        width: 100% !important;
    }
    
    /* 🚀 EKİBİ KUSURSUZ EŞİT BOYUTA GETİREN SİHİRLİ KURAL */
    .team-card {
        min-height: 230px !important; /* Tüm kartları dikeyde en uzun metne göre sabitler */
        margin-bottom: 24px !important;
    }
    
    .stButton>button {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-radius: 0.625rem !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: 1px solid #0f172a !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1e293b !important;
        border-color: #1e293b !important;
        transform: translateY(-1px);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    p {
        color: #64748b !important;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        border-radius: 9999px;
        padding: 6px 14px;
        font-size: 14px;
        font-weight: 600;
    }
    .badge-red { background-color: #fee2e2; color: #991b1b; }
    .badge-yellow { background-color: #fef9c3; color: #854d0e; }
    .badge-green { background-color: #dcfce7; color: #166534; }
    </style>
""", unsafe_allow_html=True)

try:
    from utils.styles import init_v0_styles
    from utils.charts import draw_traffic_peaks_chart, draw_weekday_weekend_chart, draw_correlation_matrix
except ImportError:
    pass

if 'sorgu_gecmisi' not in st.session_state:
    st.session_state.sorgu_gecmisi = []

current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_models_and_data():
    # app.py dosyasının bilgisayardaki tam konumu (C:\...\src\)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Projenin ana dizinine çıkış (C:\...\istanbul-traffic-density-prediction\)
    project_root = os.path.dirname(current_dir)
    
    # Modeller src/ klasörünün içinde app.py ile yan yana duruyor:
    clf_path = os.path.join(current_dir, "siniflandirma_modeli.pkl")
    reg_path = os.path.join(current_dir, "regresyon_modeli.pkl")
    
    # Veri seti ise projenin ana dizinindeki data/ klasörünün içinde:
    data_path = os.path.join(project_root, "data", "temiz_hafif_istanbul_verisi.csv")
    
    with open(clf_path, "rb") as f:
        clf = pickle.load(f)
    with open(reg_path, "rb") as f:
        reg = pickle.load(f)
        
    df = pd.read_csv(data_path)
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
    df['HOUR'] = df['DATE_TIME'].dt.hour
    df['DAYOFWEEK'] = df['DATE_TIME'].dt.dayofweek
    df['IS_WEEKEND'] = df['DAYOFWEEK'].apply(lambda x: 'Hafta Sonu / Weekend' if x >= 5 else 'Hafta İçi / Weekday')
    return clf, reg, df

try:
    clf_model, reg_model, df_clean = load_models_and_data()
    model_loaded = True
except Exception as e:
    st.error(f"Dosyalar eksik veya yüklenemedi! Klasör yolunu kontrol edin. Hata: {e}")
    model_loaded = False

turkce_eng_etiketler = {
    'HOUR': 'Günlük Saat | Daily Hour',
    'NUMBER_OF_VEHICLES': 'Ortalama Araç Sayısı | Average Vehicle Count',
    'IS_WEEKEND': 'Zaman Dilimi | Time Period',
    'MINIMUM_SPEED': 'Minimum Hız | Minimum Speed',
    'MAXIMUM_SPEED': 'Maksimum Hız | Maximum Speed',
    'AVERAGE_SPEED': 'Ortalama Hız | Average Speed',
    'DAYOFWEEK': 'Haftanın Günü | Day of Week'
}

st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 10px;">
        <h2 style='margin:0; display:inline-block;'>🚗 Trafik-Sens</h2>
        <span style="
            background-color: #0f172a; 
            color: #f8fafc; 
            padding: 2px 8px; 
            border-radius: 6px; 
            font-size: 11px; 
            font-weight: 700;
            vertical-align: middle;
            margin-top: 8px;
        ">v1.0.0</span>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:13px; margin-top:5px; color:#64748b;'>Şehir İçi Trafik Yoğunluğu Dashboard</p>", unsafe_allow_html=True)
st.sidebar.write("---")

active_tab = st.sidebar.radio(
    "📌 NAVIGATION",
    ["🔮 Trafik Tahmin Paneli", "📈 Veri Analizleri", "⏳ İşlem Geçmişi", "👥 Proje Ekibi"]
)

# ------------------------------------------------------------------
# SEKME 1: TAHMİN PANELİ
# ------------------------------------------------------------------
if active_tab == "🔮 Trafik Tahmin Paneli":
    st.markdown("<h1>Trafik Tahmin Paneli</h1>", unsafe_allow_html=True)
    st.markdown("<p>Giriş parametrelerini kullanarak yapay zeka modellerini tetikleyin.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_form, col_charts = st.columns([1.2, 2.5])
    
    with col_form:
        st.markdown('<div class="v0-card" style="min-height: auto;"><h2>📍 Prediction Form</h2>', unsafe_allow_html=True)
        latitude = st.number_input("Enlem (LATITUDE)", min_value=40.0, max_value=42.0, value=41.0586, format="%.4f")
        longitude = st.number_input("Boylam (LONGITUDE)", min_value=28.0, max_value=30.0, value=28.9544, format="%.4f")
        hour = st.slider("Saat (HOUR)", min_value=0, max_value=23, value=16)
        
        gunler = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
        selected_day = st.selectbox("Haftanın Günü", list(gunler.values()))
        dayofweek = list(gunler.keys())[list(gunler.values()).index(selected_day)]
        
        min_speed = st.slider("Minimum Hız (km/s)", min_value=0, max_value=150, value=1)
        max_speed = st.slider("Maksimum Hız (km/s)", min_value=0, max_value=200, value=98)
        avg_speed = st.slider("Ortalama Hız (km/s)", min_value=0, max_value=150, value=26)
        
        predict_btn = st.button("🚀 Trafiği Tahmin Et")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_charts:
        if model_loaded and predict_btn:
            input_data = pd.DataFrame([{
                'LATITUDE': latitude, 'LONGITUDE': longitude, 'MINIMUM_SPEED': min_speed,
                'MAXIMUM_SPEED': max_speed, 'AVERAGE_SPEED': avg_speed, 'HOUR': hour, 'DAYOFWEEK': dayofweek
            }])
            
            raw_yogunluk = clf_model.predict(input_data)[0]
            arac_tahmini = reg_model.predict(input_data)[0]
            net_arac = int(np.round(arac_tahmini))
            
            yogunluk_haritasi = {"Çok": "Yüksek", "Cok": "Yüksek", "Yüksek": "Yüksek", "Yuksek": "Yüksek", "Orta": "Orta", "Az": "Az", "Düşük": "Az"}
            yogunluk_tahmini = yogunluk_haritasi.get(raw_yogunluk, raw_yogunluk)
            
            if net_arac <= 250: yogunluk_tahmini = "Az"
            elif net_arac >= 600: yogunluk_tahmini = "Yüksek"
            elif 250 < net_arac < 600 and yogunluk_tahmini == "Az" and avg_speed < 20: yogunluk_tahmini = "Orta"
            
            yeni_kayit = {
                "Bölge / Konum (Enlem | Boylam)": f"Enlem: {latitude:.4f}  |  Boylam: {longitude:.4f}",
                "Haftanın Günü | Day": selected_day,
                "Saat | Hour": f"{hour:02d}:00", "Tahmini Araç Sayısı": str(net_arac), "Yoğunluk Durumu": yogunluk_tahmini
            }
            st.session_state.sorgu_gecmisi.insert(0, yeni_kayit)
            
            st.markdown('<div class="v0-card" style="min-height: auto;"><h3>🎯 Canlı Tahmin Sonuçları</h3>', unsafe_allow_html=True)
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                badge_class = "badge-green" if yogunluk_tahmini == "Az" else ("badge-yellow" if yogunluk_tahmini == "Orta" else "badge-red")
                st.markdown(f"""
                    <div style="padding:20px; background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0; text-align:center;">
                        <span style="color:#64748b; font-size:14px; font-weight:500;">Tahmini Yoğunluk Seviyesi</span><br/><br/>
                        <span class="badge {badge_class}">{yogunluk_tahmini}</span>
                    </div>
                """, unsafe_allow_html=True)
            with res_c2:
                st.markdown(f"""
                    <div style="padding:20px; background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0; text-align:center;">
                        <span style="color:#64748b; font-size:14px; font-weight:500;">Beklenen Net Araç Sayısı</span><br/><br/>
                        <h2 style="margin:0; color:#0f172a; font-size:32px;">{net_arac} <span style="font-size:16px; color:#64748b; font-weight:400;">Adet</span></h2>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown('<div class="v0-card" style="min-height: auto;"><h3>📊 Traffic Peaks Chart | Trafik Yoğunluk Zirveleri</h3>', unsafe_allow_html=True)
            fig_peaks = draw_traffic_peaks_chart(df_clean, turkce_eng_etiketler, is_area=False)
            st.plotly_chart(fig_peaks, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# SEKME 2: VERİ ANALİZLERİ
# ------------------------------------------------------------------
elif active_tab == "📈 Veri Analizleri":
    st.markdown("<h1>Veri Analizleri</h1>", unsafe_allow_html=True)
    st.markdown("<p>Trafik verilerinin detaylı görsel grafik analizi</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown('<div class="v0-card" style="min-height: auto;"><h3>⏱️ Traffic Peaks Chart | Trafik Yoğunluk Zirveleri Grafiği</h3>', unsafe_allow_html=True)
    fig1 = draw_traffic_peaks_chart(df_clean, turkce_eng_etiketler, is_area=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    eda_c1, eda_c2 = st.columns(2)
    
    with eda_c1:
        st.markdown('<div class="v0-card" style="min-height: auto;"><h3>📅 Weekday vs Weekend Chart | Hafta İçi ve Hafta Sonu Karşılaştırması</h3>', unsafe_allow_html=True)
        fig2 = draw_weekday_weekend_chart(df_clean, turkce_eng_etiketler)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with eda_c2:
        st.markdown('<div class="v0-card" style="min-height: auto;"><h3>🔗 Correlation Matrix | Değişkenler Arası İlişki Matrisi</h3>', unsafe_allow_html=True)
        numeric_cols = ['MINIMUM_SPEED', 'MAXIMUM_SPEED', 'AVERAGE_SPEED', 'NUMBER_OF_VEHICLES', 'HOUR']
        turkce_eng_cols = ['Min Hız | Speed', 'Max Hız | Speed', 'Ort Hız | Speed', 'Araç | Vehicle', 'Saat | Hour']
        fig3 = draw_correlation_matrix(df_clean, numeric_cols, turkce_eng_cols)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# SEKME 3: İŞLEM GEÇMİŞİ
# ------------------------------------------------------------------
elif active_tab == "⏳ İşlem Geçmişi":
    st.markdown("<h1>İşlem Geçmişi</h1>", unsafe_allow_html=True)
    st.markdown("<p>Sistemde yapılan canlı simülasyon ve test tahmin kayıtları</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown('<div class="v0-card" style="min-height: auto;"><h3>⏳ Son Sorgular (Canlı Tahmin Logları)</h3>', unsafe_allow_html=True)
    if len(st.session_state.sorgu_gecmisi) == 0:
        st.info("ℹ️ Şu anlık sorgulama yapılmadı. Lütfen tahmin panelinden simülasyonu tetikleyin.")
    else:
        history_df = pd.DataFrame(st.session_state.sorgu_gecmisi)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# SEKME 4: PROJE EKİBİ (DİKEY SÜTUNLAMA İLE MİLİMETRİK EŞİTLENDİ)
# ------------------------------------------------------------------
elif active_tab == "👥 Proje Ekibi":
    st.markdown("<h1>Proje Ekibi & Scrum Rolleri</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # 🚀 ÇÖZÜM: 2 ana dikey kolon açıyoruz, satırları alt alta bağlıyoruz
    team_col_left, team_col_right = st.columns(2)
    
    with team_col_left:
        # Sol sütunda Mustafa ve Kağan duracak
        st.markdown("""
            <div class="v0-card team-card">
                <h4 style="margin-top:0;">🛠️ Muhammet Mustafa Mencik</h4>
                <p style="color:#0f172a; font-size:14px; font-weight:600; margin-bottom:4px;">Takım Lideri / Veri Ön İşleme</p>
                <p style="font-size:13px; margin:0;">Trafik veri setlerinin pandas ile temizlenmesi, ayıklanması ve model eğitimine hazır hale getirilmesi süreçlerini yönetti.</p>
            </div>
            <div class="v0-card team-card">
                <h4 style="margin-top:0;">📊 Kağan Aydın</h4>
                <p style="color:#0f172a; font-size:14px; font-weight:600; margin-bottom:4px;">Veri Analisti / Raporlama</p>
                <p style="font-size:13px; margin:0;">Verilerin istatistiksel analizlerinin çıkarılması, grafiklerin modellenmesi ve final raporlama süreçlerini üstlendi.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with team_col_right:
        # Sağ sütunda Baran ve Mehmet duracak
        st.markdown("""
            <div class="v0-card team-card">
                <h4 style="margin-top:0;">🧠 Baran Demir</h4>
                <p style="color:#0f172a; font-size:14px; font-weight:600; margin-bottom:4px;">Makine Öğrenmesi Geliştirici</p>
                <p style="font-size:13px; margin:0;">Random Forest Sınıflandırma ve Regresyon modellerini kurarak yüksek başarı metriklerine sahip yapay zeka çıktılarını üretti.</p>
            </div>
            <div class="v0-card team-card">
                <h4 style="margin-top:0;">💻 Mehmet Açıkgöz</h4>
                <p style="color:#0f172a; font-size:14px; font-weight:600; margin-bottom:4px;">Arayüz ve Yazılım Geliştirici</p>
                <p style="font-size:13px; margin:0;">Projenin dinamik web arayüz mimarisini kodladı, veri analitiği grafiklerini ve yapay zeka modellerini sisteme entegre etti.</p>
            </div>
        """, unsafe_allow_html=True)
