import streamlit as st
import pandas as pd
import os
import json
import re
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
# تحميل التنسيقات من ملف style.css الخارجي
# =========================================================
def load_css(file_path: str):
    """يقرأ ملف CSS خارجي ويحقنه داخل صفحة Streamlit."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"ملف التنسيقات '{file_path}' غير موجود بجانب app.py.")

CSS_PATH = "style.css"
load_css(CSS_PATH)

# =========================================================
# الشعار + العنوان
# =========================================================
# الشعار مرفوع بالفعل داخل نفس المستودع (logo.png بجانب app.py)
# لذلك نقرأه محلياً بدل جلبه عبر رابط خارجي — يعمل حتى لو كان
# المستودع على GitHub خاصاً (private)، لأن raw.githubusercontent.com
# لا يعرض ملفات من مستودع خاص لغير المسجلين دخولهم.
LOGO_PATH = "logo.png"

if os.path.exists(LOGO_PATH):
    col_l, col_c, col_r = st.columns([1, 1, 1])
    with col_c:
        st.image(LOGO_PATH, width=140)
else:
    st.info("لم يتم العثور على ملف الشعار logo.png في نفس مجلد التطبيق.")

st.markdown(
    """
    <div class="autoiq-header">
        <h1>🚗 AutoIQ AI Expert</h1>
        <p>مقارنة تقنية ذكية بين السيارات مدعومة بالذكاء الاصطناعي</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# تحميل البيانات (ملف يحتوي فقط على الماركة والفئة)
# =========================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("cars_data.xlsx", engine='openpyxl')
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("ملف 'cars_data.xlsx' غير موجود. تأكد من رفعه إلى مستودع GitHub بجانب app.py.")
        return None
    except Exception as e:
        st.error(f"خطأ أثناء قراءة ملف الإكسيل: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# =========================================================
# فحص الأعمدة (الملف يحتوي فقط على Make و Model، والسنة تُختار يدوياً)
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
        "أضفه في Streamlit Secrets (Settings → Secrets)."
    )
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# =========================================================
# دالة التحليل: الذكاء الاصطناعي يعتمد فقط على الماركة/الفئة/السنة
# ويُعيد JSON منظم نستخدمه لبناء جدول ومحتوى احترافي
# =========================================================
def analyze_cars(car1, car2):

    car1_label = f"{car1['Make']} {car1['Model']} ({car1['Year']})"
    car2_label = f"{car2['Make']} {car2['Model']} ({car2['Year']})"

    prompt = f"""
أنت خبير سيارات محترف. قارن تقنياً بين السيارتين التاليتين واعتمد فقط على معرفتك العامة بهما
(الماركة والفئة وسنة الصنع)، وأجب باللغة العربية الفصحى حصراً.

السيارة الأولى: {car1_label}
السيارة الثانية: {car2_label}

أعد الإجابة بصيغة JSON صحيحة فقط، بدون أي نص إضافي قبله أو بعده، وبدون علامات ```، وفق الهيكل التالي بالضبط:

{{
  "table_rows": [
    {{"spec": "القوة الحصانية", "car1": "قيمة", "car2": "قيمة", "better": "car1"}},
    {{"spec": "عزم الدوران", "car1": "قيمة", "car2": "قيمة", "better": "car2"}},
    {{"spec": "التسارع من 0-100 كم/س", "car1": "قيمة", "car2": "قيمة", "better": "car1"}},
    {{"spec": "السرعة القصوى", "car1": "قيمة", "car2": "قيمة", "better": "car2"}},
    {{"spec": "ناقل الحركة", "car1": "قيمة", "car2": "قيمة", "better": "none"}},
    {{"spec": "استهلاك الوقود", "car1": "قيمة", "car2": "قيمة", "better": "car1"}}
  ],
  "performance_analysis": "فقرة تحليل الأداء الرياضي والتسارع",
  "luxury_analysis": "فقرة تحليل مستوى الفخامة والتجهيزات",
  "winner": "اسم السيارة الأفضل بشكل عام",
  "winner_reason": "جملة قصيرة توضح سبب الاختيار",
  "final_recommendation": "فقرة نصيحة شراء نهائية للمستخدم"
}}

ملاحظة مهمة: حقل "better" في كل صف يجب أن يكون واحداً من ثلاث قيم فقط:
"car1" إذا كانت السيارة الأولى أفضل في هذه المواصفة، أو "car2" إذا كانت السيارة الثانية أفضل،
أو "none" إذا كانت المواصفة متعادلة أو غير قابلة للمقارنة (مثل نوع ناقل الحركة).

اجعل القيم دقيقة وواقعية قدر الإمكان بناءً على معرفتك بالسيارتين المذكورتين.
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

    raw_text = response.choices[0].message.content.strip()
    return raw_text, car1_label, car2_label


def parse_ai_json(raw_text):
    """يحاول استخراج JSON صالح من رد النموذج حتى لو أضاف نصاً إضافياً."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


def render_comparison_table(table_rows, car1_label, car2_label):
    """
    يبني جدول مقارنة احترافي بتصميم عالمي المستوى، متناسق مع هوية
    التطبيق البصرية (أزرق/أحمر - روح السرعة)، مع دعم تمييز القيمة
    الأفضل في كل صف عبر حقل اختياري "better" (car1 / car2 / none).
    التنسيقات (CSS) معرّفة في ملف style.css الخارجي ضمن compare-table.
    """
    rows_html = ""
    for row in table_rows:
        spec = row.get("spec", "")
        car1_val = row.get("car1", "")
        car2_val = row.get("car2", "")
        better = row.get("better", "none")

        car1_class = "winner-cell" if better == "car1" else ""
        car2_class = "winner-cell" if better == "car2" else ""

        rows_html += f"""
        <tr>
            <td class="spec-cell">{spec}</td>
            <td class="{car1_class}">{car1_val}</td>
            <td class="{car2_class}">{car2_val}</td>
        </tr>
        """

    table_html = f"""
    <div class="compare-wrap">
        <table class="compare-table">
            <thead>
                <tr>
                    <th class="spec-col">المواصفة</th>
                    <th class="car1-col">{car1_label}</th>
                    <th class="car2-col">{car2_label}</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)


def render_report_section(title, content, red_accent=False):
    accent_class = "red-accent" if red_accent else ""
    st.markdown(
        f"""
        <div class="report-section {accent_class}">
            <h4>{title}</h4>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_winner_card(winner, reason):
    st.markdown(
        f"""
        <div class="winner-card">
            🏆 الأفضل: {winner}<br/>
            <span style="font-size:0.95rem; font-weight:500;">{reason}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# السنوات
# =========================================================
YEARS = list(range(2026, 2000, -1))

# =========================================================
# الواجهة: اختيار السيارتين
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="car-card car-card-1">', unsafe_allow_html=True)
    st.markdown("<h3>🔵 السيارة الأولى</h3>", unsafe_allow_html=True)

    make1 = st.selectbox(
        "الماركة",
        sorted(df["Make"].dropna().unique()),
        key="make1"
    )

    model1 = st.selectbox(
        "الفئة",
        sorted(df[df["Make"] == make1]["Model"].dropna().unique()),
        key="model1"
    )

    year1 = st.selectbox(
        "السنة",
        YEARS,
        key="year1"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="car-card car-card-2">', unsafe_allow_html=True)
    st.markdown("<h3>🔴 السيارة الثانية</h3>", unsafe_allow_html=True)

    make2 = st.selectbox(
        "الماركة",
        sorted(df["Make"].dropna().unique()),
        key="make2"
    )

    model2 = st.selectbox(
        "الفئة",
        sorted(df[df["Make"] == make2]["Model"].dropna().unique()),
        key="model2"
    )

    year2 = st.selectbox(
        "السنة",
        YEARS,
        key="year2"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =========================================================
# زر التحليل وعرض النتائج
# =========================================================
if st.button("⚡ ابدأ التحليل", use_container_width=True):

    with st.spinner("جاري التحليل..."):

        try:
            raw_text, car1_label, car2_label = analyze_cars(
                {"Make": make1, "Model": model1, "Year": year1},
                {"Make": make2, "Model": model2, "Year": year2}
            )

            data = parse_ai_json(raw_text)

            if data is None:
                st.warning("تعذّر تحليل الرد كجدول منظم، عرض النص الخام بدلاً من ذلك:")
                st.markdown(f'<div style="direction:rtl; text-align:right;">{raw_text}</div>', unsafe_allow_html=True)
            else:
                st.subheader("📊 جدول المقارنة")
                render_comparison_table(
                    data.get("table_rows", []),
                    car1_label,
                    car2_label
                )

                render_report_section("🏁 الأداء الرياضي والتسارع", data.get("performance_analysis", ""))
                render_report_section("✨ الفخامة والتجهيزات", data.get("luxury_analysis", ""), red_accent=True)

                if data.get("winner"):
                    render_winner_card(data.get("winner", ""), data.get("winner_reason", ""))

                render_report_section("🛒 نصيحة الشراء النهائية", data.get("final_recommendation", ""))

        except Exception as e:
            st.error(f"حدث خطأ أثناء التحليل:\n{e}")

st.markdown(
    """
    <div class="autoiq-footer">
        AutoIQ AI Expert — مدعوم بواسطة Groq &amp; Llama 3.3
    </div>
    """,
    unsafe_allow_html=True
)
