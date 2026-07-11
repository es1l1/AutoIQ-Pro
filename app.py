import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# إعداد واجهة الصفحة
st.set_page_config(page_title="AutoIQ AI Expert", layout="wide")
st.title("🚗 AutoIQ AI Expert")
st.subheader("مقارنة تقنية دقيقة بين السيارات")

# إعداد العميل (الاعتماد على Streamlit Secrets في السحابة)
def get_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("cars_data.csv")

df = load_data()

# دالة التحليل
def analyze_cars_technical(car1, car2):
    client = get_client()
    prompt = f"""
    أنت مهندس سيارات خبير. قارن تقنياً بين:
    1. {car1['Make']} {car1['Model']} موديل {car1['Year']}
    2. {car2['Make']} {car2['Model']} موديل {car2['Year']}
    
    المطلوب: جدول مقارنة (قوة، عزم، محرك)، تحليل فروقات الأجيال، وأيهما أفضل للأداء.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# واجهة القوائم المنسدلة
col1, col2 = st.columns(2)

with col1:
    st.markdown("### السيارة الأولى")
    m1 = st.selectbox("الماركة 1:", df['Make'].unique(), key="m1")
    f1 = st.selectbox("الفئة 1:", df[df['Make'] == m1]['Model'].unique(), key="f1")
    y1 = st.selectbox("السنة 1:", range(2015, 2027), key="y1")

with col2:
    st.markdown("### السيارة الثانية")
    m2 = st.selectbox("الماركة 2:", df['Make'].unique(), key="m2")
    f2 = st.selectbox("الفئة 2:", df[df['Make'] == m2]['Model'].unique(), key="f2")
    y2 = st.selectbox("السنة 2:", range(2015, 2027), key="y2")

# زر التنفيذ
if st.button("بدء التحليل التقني"):
    c1 = {"Make": m1, "Model": f1, "Year": y1}
    c2 = {"Make": m2, "Model": f2, "Year": y2}
    
    with st.spinner("جاري استحضار البيانات التقنية..."):
        try:
            report = analyze_cars_technical(c1, c2)
            st.markdown("---")
            st.markdown(report)
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
