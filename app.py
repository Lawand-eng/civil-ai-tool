import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import google.generativeai as genai
from PIL import Image

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="Civil AI Tool", page_icon="🏗️", layout="centered")

# سەرپەڕی ئەپلیکەیشنەکە
st.title("🏗️ ئامرازی شیکاریی هێز و زەبر (Civil AI Tool)")
st.write("بەخێربێیت! ئەم ئامرازە یارمەتیدەرە بۆ شیکاریی سادەی زەبر و هێزی ئەندازیاری.")

# ----------------- بەشی یەکەم: حساباتی ئەندازیاری -----------------
st.header("📊 شیکاریی تیر (Beam Analysis)")

length = st.slider("درێژیی تیر (L) بە مەتر:", 1.0, 15.0, 6.0)
load = st.number_input("بڕی بار (P) بە کیلۆنیوتن:", min_value=1.0, value=12.0)

max_moment = (load * length) / 4
st.success(f"بڕی گەورەترین زەبر (Max Bending Moment): {max_moment:.2f} kN.m")

x = np.linspace(0, length, 100)
moment = np.where(x <= length/2, (load/2)*x, (load/2)*(length - x))

fig, ax = plt.subplots()
ax.plot(x, moment, color='#1f77b4', linewidth=2.5)
ax.fill_between(x, moment, color='#1f77b4', alpha=0.15)
ax.set_title("Bending Moment Diagram (BMD)", fontsize=14, fontweight='bold')
ax.set_xlabel("Length (m)")
ax.set_ylabel("Moment (kN.m)")
ax.grid(True, linestyle='--', alpha=0.6)
ax.invert_yaxis()

st.pyplot(fig)

st.divider()

# ----------------- بەشی دووەم: چاتی زیرەکی دەستکرد و وێنە -----------------
st.header("🤖 ڕاوێژکاری زیرەکی ئەندازیاری (AI Assistant + Image Analysis)")
st.write("دەتوانیت پرسیار بنووسیت یان وێنەی کێشەیەکی مێکانیک یان ئەندازیاری دابنێیت بۆ ئەوەی شیکاریی بۆ بکات:")

api_key = st.text_input("کلیل / API Keyی Geminiی خۆت داخڵ بکە:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.8-flash')

    # زیادکردنی خانەی ئۆپلۆدکردنی وێنە
    uploaded_image = st.file_uploader("📷 وێنەی پرسیار یان کێشەی ئەندازیاری (میکانیک، ترەس، نەخشە) ئۆپلۆد بکە:", type=["png", "jpg", "jpeg"])
    
    image = None
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="وێنەی بارکراو بۆ شیکاری", use_container_width=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_prompt := st.chat_input("پرسیارەکەت یان داواکارییەکەت بۆ شیکاریی وێنەکە بنووسە..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("ئەی ئای سەرقاڵی شیکارکردنی وێنە و پرسیارەکەتە..."):
                try:
                    system_instruction = "تۆ ڕاوێژکارێکی زیرەکی ئەندازیاری شارستانی و مێکانیکیتی. وەڵامی پرسیارەکان و شیکاریی وێنەکان بە وردی و بە زمانی کوردی بدەرەوە."
                    
                    # ناردنی وێنە و دەق پێکەوە بۆ ئەی ئای ئەگەر وێنە هابێت
                    if image is not None:
                        response = model.generate_content([system_instruction, image, user_prompt])
                    else:
                        full_prompt = f"{system_instruction}\n\nپرسیار: {user_prompt}"
                        response = model.generate_content(full_prompt)

                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"هەڵەیەک ڕوودا: {e}")
else:
    st.info("💡 بۆ کاراکردنی چاتەکە، تکایە API Key لە خانەی سەرەوە بنووسە.")
