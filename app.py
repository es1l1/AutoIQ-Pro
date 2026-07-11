import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def analyze_cars_technical(
    car1: Dict[str, Any],
    car2: Dict[str, Any],
    usage: str
) -> str:
    """
    تحليل تقني دقيق يعتمد على سنة الصنع لاستدعاء المواصفات الصحيحة.
    """
    prompt = f"""
أنت مهندس سيارات خبير. مهمتك هي إجراء مقارنة تقنية دقيقة جداً بين سيارتين.
بناءً على الماركة والفئة وسنة الصنع المذكورة، استخدم معرفتك التقنية لاسترجاع المواصفات (القوة بالحصان، العزم، المحرك) الخاصة بكل سنة صنع محددة بدقة.

السيارات للمقارنة:
1. {car1['Make']} {car1['Model']} موديل {car1['Year']}
2. {car2['Make']} {car2['Model']} موديل {car2['Year']}

نوع الاستخدام: {usage}

المطلوب:
1. جدول مقارنة سريع يوضح (القوة بالحصان، العزم، نوع المحرك) لكل سيارة في سنتها المحددة.
2. تحليل دقيق: لماذا قد تكون موديلات معينة (مثل 2023 مقابل 2025) أقوى أو أضعف؟ (وضح الفروقات التقنية مثل التيربو، عدد الاحصنة، إلخ).
3. بناءً على الأرقام التقنية الحقيقية لهذه السنوات، أيهما يخدم نوع الاستخدام المذكور بشكل أفضل؟
4. نصيحة شراء نهائية مبنية على الأداء التقني.

تنبيه: التزم بالأرقام التقنية الدقيقة لكل سنة صنع. إذا كانت هناك فروقات جوهرية بسبب اختلاف الأجيال، وضحها.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2 # تقليل الحرارة لضمان الدقة في الأرقام
    )
    return response.choices[0].message.content

# مثال للاختبار:
c1 = {"Make": "Toyota", "Model": "Camry", "Year": 2023}
c2 = {"Make": "Toyota", "Model": "Camry", "Year": 2025}
print(analyze_cars_technical(c1, c2, "استخدام رياضي"))
import streamlit as st
# ... باقي الـ imports التي أضفناها سابقاً ...

st.title("AutoIQ AI Expert")

# تجربة عرض بسيطة
if st.button("اختبار الاتصال"):
    st.write("الكود يعمل بنجاح!")
    
# ... باقي كودك (الدالة analyze_cars_technical) ...