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
        background: radial-gradient(circle at 50% 0%, #16213e 0%, #0f0f0f 70%, #000000 100%);
    }

    .autoiq-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 5px;
    }

    .autoiq-subtitle {
        text-align: center;
        color: #007bff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
    }

    .car-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(15px);
        transition: 0.3s;
    }

    .car-card-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 2px solid #007bff;
        padding-bottom: 10px;
    }

    div.stButton > button {
        width: 60%;
        display: block;
        margin: 20px auto;
        background: linear-gradient(90deg, #007bff, #ff2d2d);
        color: white;
        font-weight: 900;
        font-size: 1.4rem;
        padding: 15px 40px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transition: 0.4s;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(255, 45, 45, 0.4);
    }

    .report-box {
        background: rgba(0, 0, 0, 0.5);
        border-top: 5px solid #007bff;
        border-bottom: 5px solid #ff2d2d;
        border-radius: 20px;
        padding: 35px;
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 2;
    }
    
    .vs-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: 900;
        color: #ff2d2d;
        height: 100%;
        text-shadow: 0 0 15px rgba(255, 45, 45, 0.6);
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
