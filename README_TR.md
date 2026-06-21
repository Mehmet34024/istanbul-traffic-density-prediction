# İstanbul Trafik Yoğunluğu Tahmin Sistemi 🚗📊

Language Options / Dil Seçenekleri: [English](README.md) | [Türkçe (Mevcut)](README_TR.md)

İBB Açık Veri Portalı’ndan alınan sensör verilerini işleyerek anlık tahminler üreten uçtan uca, modüler bir yapay zeka karar destek sistemidir.

## 📌 Proje Özeti
- **Veri Seti:** Milyonlarca satırlık İBB veri havuzundan filtrelenen Ekim 2024 dönemine ait sensör logları.
- **Proje Yönetimi:** Çevik yazılım prensiplerine bağlı kalarak Trello üzerinde yönetilen 4 Sprint'lik Scrum süreci.
- **Modüler Mimari (Separation of Concerns):** Projenin sürdürülebilirliği ve kod kalitesi için grafik motoru (`charts.py`) ve arayüz giydirme katmanı (`styles.py`) bağımsız modüller halinde yapılandırılmıştır.
- **Modelleme:** Sınıflandırmada **%78.50 Doğruluk (Accuracy)**, regresyonda ise ortalama **~54 araç sapma payı (MAE)**.

## 👥 Takım ve Roller
- **Muhammet Mustafa Mencik:** Takım Lideri / Veri Ön İşleme
- **Kağan Aydın:** Veri Analisti / Keşifsel Veri Grafik Motoru Geliştiricisi
- **Baran Demir:** Makine Öğrenmesi Geliştirici
- **Mehmet Açıkgöz (Ben):** Arayüz ve Yazılım Geliştirici / Modüler Dashboard Mimarisi & Mutlak Yol Dinamik Entegrasyonları

## 💻 Üstlendiğim Arayüz & Yazılım Mimarlığı Rolü
- Kurumsal standartlara uygun, modern, nesne yönelimli ve duyarlı (responsive) bir **Streamlit** dashboard mimarisi tasarladım.
- Veri analitiği sekmesinde dinamik zaman serisi trendlerini harici `utils` paketi üzerinden Plotly grafiklerine bağladım.
- `st.session_state` kullanarak simüle edilen tahminleri anlık yakalayan bir **Canlı Sorgu Loglama** altyapısı kurdum ve işletim sistemlerinden bağımsız mutlak veri yollarını (`os.path.abspath`) entegre ettim.

## 🖥️ Uygulama Ekran Görüntüleri

### Trafik Tahmin Paneli ve Canlı Tahmin Sonuçları
![Prediction Panel](assets/predict_panel.jpeg)

### Veri Analizleri ve Interaktif Grafik Yapısı
![Analytics Panel](assets/analytics_panel.jpeg)

### İşlem Geçmişi Tablosu ve Log Altyapısı
![History Panel](assets/history_panel.jpeg)

### Proje Ekibi ve Scrum Rolleri Paneli
![Team Panel](assets/team_panel.jpeg)