import os
import logging
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# ------------------------------
# تهيئة متغيرات البيئة
# ------------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
# إعداد عميل Groq
# ------------------------------
# يمكنك وضع المفتاح في ملف .env كـ GROQ_API_KEY
API_KEY = os.getenv("GROQ_API_KEY") 

if not API_KEY:
    raise EnvironmentError("❌ لم يتم العثور على GROQ_API_KEY في ملف .env.")

# إنشاء العميل المتصل بـ Groq
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def analyze_cars(
    car1: Dict[str, Any],
    car2: Dict[str, Any],
    usage: str,
    temperature: float = 0.3
) -> str:
    """
    تحليل مقارنة بين سيارتين باستخدام نموذج Llama 3 عبر Groq.
    """
    # التحقق من صحة البيانات
    required_keys = {"Name", "HP", "Torque", "CC", "Fuel"}
    for car, label in [(car1, "car1"), (car2, "car2")]:
        if not all(key in car for key in required_keys):
            raise ValueError(f"❌ البيانات الناقصة في {label}.")

    # بناء النص الموجه (prompt)
    prompt = f"""
أنت AutoIQ Expert، خبير سيارات عالمي.

🔹 السيارة الأولى: {car1['Name']} (قوة: {car1['HP']} حصان، عزم: {car1['Torque']} نيوتن.متر، سعة: {car1['CC']} سي سي، استهلاك: {car1['Fuel']} لتر/100كم)
🔹 السيارة الثانية: {car2['Name']} (قوة: {car2['HP']} حصان، عزم: {car2['Torque']} نيوتن.متر، سعة: {car2['CC']} سي سي، استهلاك: {car2['Fuel']} لتر/100كم)
🔹 نوع الاستخدام المطلوب: {usage}

اكتب تقريراً احترافياً باللغة العربية يتضمن: الفائز النهائي، تحليل الأداء، الأفضل للاستخدام اليومي، استهلاك الوقود، الاعتمادية، المميزات، العيوب، ونصيحة شراء.
"""

    try:
        # استدعاء نموذج Llama 3 عبر Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # نموذج سريع وقوي جداً
            messages=[
                {"role": "system", "content": "أنت خبير سيارات محترف وموضوعي."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        logger.info("✅ تم الحصول على التقرير من Groq بنجاح.")
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال بـ Groq: {e}")
        raise

if __name__ == "__main__":
    sample_car1 = {"Name": "Toyota Camry", "HP": 203, "Torque": 250, "CC": 2500, "Fuel": 7.5}
    sample_car2 = {"Name": "Honda Accord", "HP": 192, "Torque": 260, "CC": 2400, "Fuel": 7.2}
    
    try:
        report = analyze_cars(sample_car1, sample_car2, "استخدام يومي")
        print(report)
    except Exception as e:
        print(f"فشل الاختبار: {e}")