import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# =========================================================
# إعداد الصفحة
# =========================================================
st.set_page_config(
    page_title="AutoIQ AI Expert",
    page_icon="🚗",
    layout="wide"
)

# =========================================================
# الشعار
# =========================================================
LOGO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/logo.png"

try:
    st.image(LOGO_URL, width="stretch")
except:
    pass

st.title("🚗 AutoIQ AI Expert")
st.markdown("### مقارنة تقنية ذكية بين السيارات")

# =========================================================
# تحميل البيانات
# =========================================================
@st.cache_data
def load_data():
    try:
        # استخدام openpyxl لقراءة ملف الإكسيل
        df = pd.read_excel("cars_data.xlsx", engine='openpyxl')
        # تنظيف أسماء الأعمدة من أي فراغات إضافية
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("ملف 'cars_data.xlsx' غير موجود. تأكد من رفعه إلى مستودع GitHub.")
        return None
    except Exception as e:
        st.error(f"خطأ أثناء قراءة ملف الإكسيل: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# =========================================================
# فحص الأعمدة
# =========================================================
required_columns = ["Make", "Model"]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error(
        f"الأعمدة المطلوبة غير موجودة: {missing}\n\n"
        f"الأعمدة الموجودة فعلياً:\n{list(df.columns)}"
    )
    st.stop()

# =========================================================
# مفتاح Groq
# =========================================================
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY غير موجود.\n"
        "أضفه في Streamlit Secrets."
    )
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# =========================================================
# دالة التحليل
# =========================================================
def analyze_cars(car1, car2):

    prompt = f"""
قارن تقنياً بين:

السيارة الأولى:
{car1['Make']} {car1['Model']} موديل {car1['Year']}

السيارة الثانية:
{car2['Make']} {car2['Model']} موديل {car2['Year']}

اعرض:

1- جدول مقارنة
2- القوة الحصانية
3- العزم
4- الأداء الرياضي
5- التسارع
6- الفخامة
7- أيهما أفضل
8- نصيحة شراء نهائية
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# =========================================================
# السنوات
# =========================================================
YEARS = list(range(2026, 2000, -1))

# =========================================================
# الواجهة
# =========================================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("السيارة الأولى")

    make1 = st.selectbox(
        "الماركة",
        sorted(df["Make"].dropna().unique()),
        key="make1"
    )

    model1 = st.selectbox(
        "الفئة",
        sorted(
            df[df["Make"] == make1]["Model"]
            .dropna()
            .unique()
        ),
        key="model1"
    )

    year1 = st.selectbox(
        "السنة",
        YEARS,
        key="year1"
    )

with col2:

    st.subheader("السيارة الثانية")

    make2 = st.selectbox(
        "الماركة",
        sorted(df["Make"].dropna().unique()),
        key="make2"
    )

    model2 = st.selectbox(
        "الفئة",
        sorted(
            df[df["Make"] == make2]["Model"]
            .dropna()
            .unique()
        ),
        key="model2"
    )

    year2 = st.selectbox(
        "السنة",
        YEARS,
        key="year2"
    )

st.divider()

if st.button("⚡ ابدأ التحليل", use_container_width=True):

    with st.spinner("جاري التحليل..."):

        try:

            result = analyze_cars(
                {
                    "Make": make1,
                    "Model": model1,
                    "Year": year1
                },
                {
                    "Make": make2,
                    "Model": model2,
                    "Year": year2
                }
            )

            st.markdown(result)

        except Exception as e:
            st.error(f"حدث خطأ أثناء التحليل:\n{e}")
