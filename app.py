import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 1. إعداد الصفحة
st.set_page_config(page_title="AutoIQ AI Expert", page_icon="🚗", layout="wide")

st.title("🚗 AutoIQ AI Expert")
st.markdown("---")

# 2. تحميل البيانات (Excel بدلاً من CSV)
@st.cache_data
def load_data():
    try:
        # قراءة ملف الإكسل مباشرة
        df = pd.read_excel("cars_data.xlsx")
        # تنظيف أسماء الأعمدة من أي فراغات
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة ملف الإكسل: {e}")
        return pd.DataFrame()

df = load_data()

# 3. دالة التحليل
def analyze_cars_technical(car1, car2):
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    
    prompt = f"قارن تقنياً بين {car1['Make']} {car1['Model']} و {car2['Make']} {car2['Model']} من حيث الأداء الرياضي."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# 4. الواجهة (مع التأكد من وجود الأعمدة)
if not df.empty and 'Make' in df.columns and 'Model' in df.columns:
    col1, col2 = st.columns(2)
    with col1:
        m1 = st.selectbox("الماركة 1:", df['Make'].unique(), key="m1")
        f1 = st.selectbox("الفئة 1:", df[df['Make'] == m1]['Model'].unique(), key="f1")
    with col2:
        m2 = st.selectbox("الماركة 2:", df['Make'].unique(), key="m2")
        f2 = st.selectbox("الفئة 2:", df[df['Make'] == m2]['Model'].unique(), key="f2")

    if st.button("تحليل"):
        report = analyze_cars_technical({"Make": m1, "Model": f1, "Year": 2025}, {"Make": m2, "Model": f2, "Year": 2025})
        st.markdown(report)
else:
    st.warning("يرجى التأكد من رفع ملف 'cars_data.xlsx' ومن وجود عمودي 'Make' و 'Model'.")
