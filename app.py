import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 1. إعداد الصفحة بشكل احترافي
st.set_page_config(page_title="AutoIQ AI Expert", page_icon="🚗", layout="wide")

# تخصيص المظهر بـ CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007BFF; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 AutoIQ AI Expert")
st.markdown("---")

# 2. تحميل البيانات مع معالجة الفاصلة المنقوطة (sep=';')
@st.cache_data
def load_data():
    # إضافة encoding='utf-8-sig' يساعد في إزالة الرموز غير المرئية في بداية الملف
    df = pd.read_csv("cars_data.csv", sep=';', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
    return df    except Exception as e:
        st.error(f"خطأ في قراءة ملف البيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 3. دالة التحليل مع معالجة الأخطاء
def analyze_cars_technical(car1, car2):
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    
    prompt = f"""
    أنت مهندس سيارات خبير. مهمتك إجراء مقارنة تقنية دقيقة بين:
    1. {car1['Make']} {car1['Model']} موديل {car1['Year']}
    2. {car2['Make']} {car2['Model']} موديل {car2['Year']}
    
    المطلوب تقديم:
    - جدول مقارنة احترافي (القوة بالحصان، العزم، نوع المحرك).
    - تحليل تقني لأي تغييرات جوهرية بين سنتي الصنع (فروقات الأجيال).
    - نصيحة تقنية بناءً على نوع الأداء.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# 4. واجهة المستخدم المنظمة
if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("السيارة الأولى")
        m1 = st.selectbox("اختر الماركة:", df['Make'].unique(), key="m1")
        f1 = st.selectbox("اختر الفئة:", df[df['Make'] == m1]['Model'].unique(), key="f1")
        y1 = st.selectbox("سنة الصنع:", range(2026, 2014, -1), key="y1")

    with col2:
        st.subheader("السيارة الثانية")
        m2 = st.selectbox("اختر الماركة:", df['Make'].unique(), key="m2")
        f2 = st.selectbox("اختر الفئة:", df[df['Make'] == m2]['Model'].unique(), key="f2")
        y2 = st.selectbox("سنة الصنع:", range(2026, 2014, -1), key="y2")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("بدء التحليل التقني المتقدم"):
        with st.spinner("جاري تحليل المواصفات التقنية بدقة..."):
            try:
                c1 = {"Make": m1, "Model": f1, "Year": y1}
                c2 = {"Make": m2, "Model": f2, "Year": y2}
                report = analyze_cars_technical(c1, c2)
                st.markdown("---")
                st.markdown(report)
            except Exception as e:
                st.error(f"فشل الاتصال بخادم الذكاء الاصطناعي: {e}")
else:
    st.warning("لم يتم العثور على بيانات. تأكد من ملف cars_data.csv.")
