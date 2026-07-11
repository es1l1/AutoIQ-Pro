import os
import streamlit as st
import pandas as pd

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

    .autoiq-header {
        text-align: center;
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

    .autoiq-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,123,255,0.6), rgba(255,45,45,0.6), transparent);
        margin: 10px 0 30px 0;
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
        width: 100%;
        max-width: 500px;
        display: block;
        margin: 0 auto;
        padding: 20px 0;
        font-size: 1.5rem;
        font-weight: 900;
        border-radius: 15px;
        border: none;
        background: linear-gradient(90deg, #007bff, #ff2d2d);
        color: white;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 45, 45, 0.4);
        background: linear-gradient(90deg, #ff2d2d, #007bff);
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
        pass  # في حال لم يتم استبدال الرابط بعد أو تعذر تحميل الصورة

st.markdown('<div class="autoiq-header"><h1 class="autoiq-title">🚗 AutoIQ AI Expert</h1></div>', unsafe_allow_html=True)
st.markdown('<p class="autoiq-subtitle">مقارنة تقنية ذكية بين السيارات مدعومة بالذكاء الاصطناعي ⚡</p>', unsafe_allow_html=True)
st.markdown('<hr class="autoiq-divider">', unsafe_allow_html=True)

# =========================================================
# 5. تحميل البيانات
# =========================================================
DATA_FILE = "cars_data.xlsx"


@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(), f"ملف البيانات '{DATA_FILE}' غير موجود في مجلد المشروع."
    try:
        data = pd.read_excel(DATA_FILE)
        data.columns = data.columns.str.strip()
        return data, None
    except Exception as e:
        return pd.DataFrame(), f"خطأ في قراءة ملف البيانات: {e}"


df, load_error = load_data()

# لا يوجد عمود سنة في الملف، لذلك نستخدم قائمة سنوات ثابتة
YEARS_LIST = list(range(2026, 1999, -1))  # من 2026 إلى 2000


# =========================================================
# 6. إدارة مفتاح API والعميل (Client)
# =========================================================
def get_api_key():
    """يحاول جلب المفتاح من secrets.toml أولاً، ثم من متغيرات البيئة."""
    key = None
    try:
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        # لا يوجد ملف secrets.toml أو تعذر قراءته - لا مشكلة، نكمل للخطوة التالية
        key = None
    if not key:
        key = os.environ.get("GROQ_API_KEY")
    return key


@st.cache_resource
def get_client(api_key: str):
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


# =========================================================
# 7. دالة التحليل (مع معالجة الأخطاء)
# =========================================================
def analyze_cars_technical(car1, car2):
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "لم يتم العثور على مفتاح GROQ_API_KEY. الرجاء إضافته إلى ملف "
            "'.streamlit/secrets.toml' بالشكل التالي:\n\nGROQ_API_KEY = \"your_key_here\""
        )

    client = get_client(api_key)

    prompt = (
        f"قارن تقنياً بين {car1['Make']} {car1['Model']} (سنة الصنع {car1['Year']}) "
        f"و {car2['Make']} {car2['Model']} (سنة الصنع {car2['Year']}) من حيث الأداء الرياضي، "
        f"القوة الحصانية، التسارع، والفخامة. اجعل الإجابة منظمة بعناوين فرعية وقوائم نقطية."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1200,
    )
    return response.choices[0].message.content


# =========================================================
# 8. أدوات مساعدة لضبط القوائم المتتابعة (Make -> Model)
# =========================================================
def reset_model_selection(model_key: str):
    """عند تغيير الماركة، نحذف اختيار الفئة القديم لتفادي خطأ
    'value is not part of options' الذي يحدث عندما لا تعود القيمة القديمة موجودة."""
    if model_key in st.session_state:
        del st.session_state[model_key]


# =========================================================
# 9. الواجهة
# =========================================================
if load_error:
    st.warning(load_error)
elif df.empty or "Make" not in df.columns or "Model" not in df.columns:
    st.warning("يرجى التأكد من رفع ملف 'cars_data.xlsx' ومن وجود عمودي 'Make' و 'Model'.")
else:
    col1, col_vs, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown('<div class="car-card"><div class="car-card-title">🚘 السيارة الأولى</div>', unsafe_allow_html=True)
        m1 = st.selectbox("الماركة 1:", df["Make"].unique(), key="m1", on_change=reset_model_selection, args=("f1",))
        f1 = st.selectbox("الفئة 1:", df[df["Make"] == m1]["Model"].unique(), key="f1")
        y1 = st.selectbox("سنة الصنع 1:", YEARS_LIST, key="y1")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_vs:
        st.markdown('<div class="vs-badge">VS</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="car-card"><div class="car-card-title">🚘 السيارة الثانية</div>', unsafe_allow_html=True)
        m2 = st.selectbox("الماركة 2:", df["Make"].unique(), key="m2", on_change=reset_model_selection, args=("f2",))
        f2 = st.selectbox("الفئة 2:", df[df["Make"] == m2]["Model"].unique(), key="f2")
        y2 = st.selectbox("سنة الصنع 2:", YEARS_LIST, key="y2")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        analyze_clicked = st.button("⚡ ابدأ المقارنة التقنية")

    if analyze_clicked:
        with st.spinner("🔧 جاري تحليل الأداء والمقارنة التقنية..."):
            try:
                report = analyze_cars_technical(
                    {"Make": m1, "Model": f1, "Year": y1},
                    {"Make": m2, "Model": f2, "Year": y2},
                )
                st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
            except ValueError as e:
                st.error(str(e))
            except AuthenticationError:
                st.error("مفتاح GROQ_API_KEY غير صحيح أو منتهي الصلاحية. الرجاء التحقق منه.")
            except APIConnectionError:
                st.error("تعذر الاتصال بخدمة Groq. تحقق من اتصال الإنترنت وحاول مرة أخرى.")
            except APIError as e:
                st.error(f"حدث خطأ من خدمة الذكاء الاصطناعي: {e}")
            except Exception as e:
                st.error(f"حدث خطأ غير متوقع أثناء التحليل: {e}")
