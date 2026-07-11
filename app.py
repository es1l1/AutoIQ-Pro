import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# =========================================================
# 1. إعداد الصفحة
# =========================================================
st.set_page_config(
    page_title="AutoIQ AI Expert",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 2. الشعار (Logo)
# ضع رابط الشعار الخام (raw) من GitHub هنا. مثال:
# https://raw.githubusercontent.com/USERNAME/REPO/main/logo.png
# =========================================================
LOGO_URL = "https://raw.githubusercontent.com/es1l1/AutoIQ-Pro/main/logo.png"

# =========================================================
# 3. التنسيق الاحترافي (CSS) - طابع فخامة وسرعة
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    .stApp {
        background: radial-gradient(circle at 50% -20%, #1a2a3a 0%, #0a0a0a 70%, #000000 100%);
        color: #e0e0e0;
    }

    .autoiq-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #007bff, #ffffff, #ff2d2d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }

    .car-card {
        background: rgba(255, 255, 255, 0.03);
        border-right: 4px solid #007bff;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #007bff, #0056b3);
        color: white;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 15px;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #ff2d2d, #cc0000);
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 45, 45, 0.4);
    }

    .report-box {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid #333;
        border-left: 5px solid #ff2d2d;
        border-radius: 10px;
        padding: 25px;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)
# =========================================================
# 4. رأس الصفحة + الشعار
# =========================================================
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    try:
        st.image(LOGO_URL, use_container_width=True)
    except Exception:
        pass  # في حال لم يتم استبدال الرابط بعد

st.markdown('<div class="autoiq-header"><h1 class="autoiq-title">🚗 AutoIQ AI Expert</h1></div>', unsafe_allow_html=True)
st.markdown('<p class="autoiq-subtitle">مقارنة تقنية ذكية بين السيارات مدعومة بالذكاء الاصطناعي ⚡</p>', unsafe_allow_html=True)
st.markdown('<hr class="autoiq-divider">', unsafe_allow_html=True)

# =========================================================
# 5. تحميل البيانات (نفس المنطق الأصلي)
# =========================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("cars_data.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة ملف البيانات: {e}")
        return pd.DataFrame()

df = load_data()

# لا يوجد عمود سنة في الملف، لذلك نستخدم قائمة سنوات ثابتة (يمكنك تعديل النطاق كما تشاء)
YEARS_LIST = list(range(2026, 1999, -1))  # من 2026 إلى 2000

# =========================================================
# 6. دالة التحليل (نفس المنطق الأصلي + تمرير السنة)
# =========================================================
def analyze_cars_technical(car1, car2):
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    prompt = (
        f"قارن تقنياً بين {car1['Make']} {car1['Model']} (سنة الصنع {car1['Year']}) "
        f"و {car2['Make']} {car2['Model']} (سنة الصنع {car2['Year']}) من حيث الأداء الرياضي، "
        f"القوة الحصانية، التسارع، والفخامة."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# =========================================================
# 7. الواجهة
# =========================================================
if not df.empty and 'Make' in df.columns and 'Model' in df.columns:

    col1, col_vs, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown('<div class="car-card"><div class="car-card-title">🚘 السيارة الأولى</div>', unsafe_allow_html=True)
        m1 = st.selectbox("الماركة 1:", df['Make'].unique(), key="m1")
        f1 = st.selectbox("الفئة 1:", df[df['Make'] == m1]['Model'].unique(), key="f1")
        y1 = st.selectbox("سنة الصنع 1:", YEARS_LIST, key="y1")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_vs:
        st.markdown('<div class="vs-badge">VS</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="car-card"><div class="car-card-title">🚘 السيارة الثانية</div>', unsafe_allow_html=True)
        m2 = st.selectbox("الماركة 2:", df['Make'].unique(), key="m2")
        f2 = st.selectbox("الفئة 2:", df[df['Make'] == m2]['Model'].unique(), key="f2")
        y2 = st.selectbox("سنة الصنع 2:", YEARS_LIST, key="y2")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    center = st.columns([1, 2, 1])
    with center[1]:
        analyze_clicked = st.button("⚡ ابدأ المقارنه")

    if analyze_clicked:
        with st.spinner("🔧 جاري تحليل الأداء والمقارنة التقنية..."):
            report = analyze_cars_technical(
                {"Make": m1, "Model": f1, "Year": y1},
                {"Make": m2, "Model": f2, "Year": y2}
            )
        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)

else:
    st.warning("يرجى التأكد من رفع ملف 'cars_data.xlsx' ومن وجود عمودي 'Make' و 'Model'.")
