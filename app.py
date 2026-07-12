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
# التنسيق العام: عربي RTL + هوية بصرية أزرق/أحمر (روح السرعة)
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

    :root{
        --speed-blue: #0B3D91;
        --speed-blue-light: #1E6FEB;
        --speed-red: #D71920;
        --speed-red-dark: #8E0F13;
        --dark-bg: #0E1117;
        --card-bg: #161B24;
        --muted-text: #9aa4b2;
    }

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Tajawal', sans-serif !important;
        text-align: right;
    }

    .block-container {
        direction: rtl;
        padding-top: 1.2rem;
        max-width: 1200px;
    }

    /* شعار مركزي أنيق بدل التمدد الكامل */
    .logo-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 6px;
    }
    .logo-wrap img {
        max-width: 130px;
        border-radius: 16px;
    }

    /* عنوان التطبيق */
    .autoiq-header {
        background: linear-gradient(90deg, var(--speed-blue) 0%, var(--speed-blue-light) 45%, var(--speed-red) 100%);
        padding: 30px 24px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 26px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.4);
    }
    .autoiq-header h1 {
        color: #fff !important;
        margin: 0;
        font-weight: 900;
        text-align: center;
        letter-spacing: 1px;
        font-size: 2.2rem;
    }
    .autoiq-header p {
        color: #eef2ff;
        margin: 8px 0 0 0;
        text-align: center;
        font-size: 1.05rem;
        opacity: 0.95;
    }

    /* بطاقات اختيار السيارة */
    .car-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 20px 20px 8px 20px;
        border-top: 4px solid;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }
    .car-card-1 { border-color: var(--speed-blue-light); }
    .car-card-2 { border-color: var(--speed-red); }

    .car-card h3 {
        text-align: center;
        margin-top: 0;
        font-weight: 800;
    }
    .car-card-1 h3 { color: var(--speed-blue-light); }
    .car-card-2 h3 { color: var(--speed-red); }

    /* زر التحليل */
    div.stButton > button {
        background: linear-gradient(90deg, var(--speed-red) 0%, var(--speed-blue) 100%);
        color: #fff;
        font-weight: 700;
        font-size: 1.15rem;
        border: none;
        border-radius: 12px;
        padding: 14px 0;
        transition: 0.2s ease-in-out;
        box-shadow: 0 6px 16px rgba(215,25,32,0.35);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(30,111,235,0.45);
        color: #fff;
    }

    /* جدول المقارنة المخصص */
    .compare-wrap {
        direction: rtl;
        margin-top: 10px;
        margin-bottom: 24px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(0,0,0,0.35);
    }
    table.compare-table {
        width: 100%;
        border-collapse: collapse;
        direction: rtl;
        font-family: 'Tajawal', sans-serif;
    }
    table.compare-table th {
        background: linear-gradient(90deg, var(--speed-blue) 0%, var(--speed-blue-light) 100%);
        color: #fff;
        padding: 15px 10px;
        text-align: center;
        font-size: 1.05rem;
    }
    table.compare-table th.spec-col {
        background: var(--dark-bg);
    }
    table.compare-table th.car2-col {
        background: linear-gradient(90deg, var(--speed-red-dark) 0%, var(--speed-red) 100%);
    }
    table.compare-table td {
        padding: 13px 10px;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        color: #e6e6e6;
    }
    table.compare-table td.spec-cell {
        text-align: right;
        font-weight: 700;
        background: rgba(255,255,255,0.03);
        color: #c9d6ff;
    }
    table.compare-table tr:nth-child(even) td {
        background: rgba(255,255,255,0.02);
    }

    /* بطاقة الفائز */
    .winner-card {
        background: linear-gradient(90deg, var(--speed-blue) 0%, var(--speed-red) 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: #fff;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 22px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.4);
    }

    /* أقسام التقرير */
    .report-section {
        background: var(--card-bg);
        border-right: 5px solid var(--speed-blue-light);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        text-align: right;
        direction: rtl;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .report-section h4 {
        color: var(--speed-blue-light);
        margin-top: 0;
        font-weight: 800;
    }
    .report-section p {
        color: #dfe4ea;
        line-height: 1.9;
        margin-bottom: 0;
    }
    .report-section.red-accent {
        border-right-color: var(--speed-red);
    }
    .report-section.red-accent h4 {
        color: var(--speed-red);
    }

    /* تذييل */
    .autoiq-footer {
        text-align: center;
        color: var(--muted-text);
        font-size: 0.85rem;
        margin-top: 30px;
        padding-top: 14px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    {{"spec": "القوة الحصانية", "car1": "قيمة", "car2": "قيمة"}},
    {{"spec": "عزم الدوران", "car1": "قيمة", "car2": "قيمة"}},
    {{"spec": "التسارع من 0-100 كم/س", "car1": "قيمة", "car2": "قيمة"}},
    {{"spec": "السرعة القصوى", "car1": "قيمة", "car2": "قيمة"}},
    {{"spec": "ناقل الحركة", "car1": "قيمة", "car2": "قيمة"}},
    {{"spec": "استهلاك الوقود", "car1": "قيمة", "car2": "قيمة"}}
  ],
  "performance_analysis": "فقرة تحليل الأداء الرياضي والتسارع",
  "luxury_analysis": "فقرة تحليل مستوى الفخامة والتجهيزات",
  "winner": "اسم السيارة الأفضل بشكل عام",
  "winner_reason": "جملة قصيرة توضح سبب الاختيار",
  "final_recommendation": "فقرة نصيحة شراء نهائية للمستخدم"
}}

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
    rows_html = ""
    for row in table_rows:
        rows_html += f"""
        <tr>
            <td class="spec-cell">{row.get('spec', '')}</td>
            <td>{row.get('car1', '')}</td>
            <td>{row.get('car2', '')}</td>
        </tr>
        """

    table_html = f"""
    <div class="compare-wrap">
        <table class="compare-table">
            <thead>
                <tr>
                    <th class="spec-col">المواصفة</th>
                    <th>{car1_label}</th>
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
