# 🛰 notGIS GEE Studio

**Professional GIS va masofadan zondlash platformasi** — ArcGIS Pro / QGIS darajasidagi desktop-like veb interfeys.

## Xususiyatlari

- 🗺 **Interactive Xarita** — Folium + GEE tile layers, Draw tools, basemap tanlash
- 📊 **20+ Indekslar** — NDVI, EVI, NDWI, MNDWI, LST, NBR, NDBI va boshqalar
- 📈 **Time Series** — Yillik, oylik, mavsumiy tahlil, trend (Mann-Kendall)
- 🤖 **Multi-AI** — Gemini, Groq, OpenRouter, RouterWay — tabiiy tilda dashboard sozlash
- 📦 **Eksport** — CSV, Excel, GeoTIFF, GEE Asset, JS/Python kod generatsiya
- 🔗 **4 GEE ulanish** — Token, Service Account, ADC, API Key
- 🎨 **Dark/Light Mode** — Professional interfeys, compact design

## Tezkor Boshlash

```bash
# 1. Klonlash
cd notgis_gee_studio

# 2. O'rnatish
pip install -r requirements.txt

# 3. Ishga tushirish
streamlit run app.py
```

## Papka Tuzilmasi

```
notgis_gee_studio/
├── app.py                  ← Entry point
├── config/                 ← Sozlamalar, temalar, AOI
├── core/                   ← GEE auth, analysis, export, indices
├── ai/                     ← Multi-AI router va providers
├── ui/                     ← 3-panel interface
│   ├── left_panel/         ← Parametrlar (7 accordion bo'lim)
│   ├── center_panel/       ← Folium xarita
│   └── right_panel/        ← Natijalar (4 tab)
├── utils/                  ← Log, export, kod generatsiya
└── assets/                 ← CSS, fontlar
```

## GEE Ulanish

1. Google Earth Engine hisobingiz bo'lishi kerak
2. `earthengine authenticate` buyrug'ini terminal da ishga tushiring
3. Ilovada Project ID ni kiriting va "Ulaning" tugmasini bosing

## AI Sozlash

1. O'ng panelda "AI" tabni oching
2. Provider tanlang (Gemini, Groq, OpenRouter, RouterWay)
3. API kalitingizni kiriting
4. "Saqlash" tugmasini bosing
5. Tabiiy tilda so'rov bering: *"Xorazm viloyatida NDVI o'zgarishini ko'rsat"*

## Texnologiyalar

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.10+ | Backend |
| Streamlit | 1.35+ | UI framework |
| Folium | 0.17+ | Interaktiv xarita |
| Earth Engine | 0.1.414+ | Ma'lumot manba |
| Plotly | 5.22+ | Grafiklar |
| Pandas | 2.2+ | Ma'lumot qayta ishlash |

## Litsenziya

MIT License

---

**notGIS** — Professional GIS, hammaga ochiq.
