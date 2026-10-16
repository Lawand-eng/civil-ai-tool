import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# سەرپەڕی ئەپلیکەیشنەکە
st.title("🏗️ ئامرازی شیکاریی هێز و زەبر (Civil AI Tool)")
st.write("بەخێربێیت! ئەم ئامرازە یارمەتیدەرە بۆ شیکاریی سادەی زەبر و هێزی ئەندازیاری.")

# وەرگرتنی داتا لە بەکارهێنەر
length = st.slider("درێژیی تیر تیرەکە (L) بە مەتر:", 1.0, 15.0, 6.0)
load = st.number_input("بڕی بار (P) بە کیلۆنیوتن:", min_value=1.0, value=12.0)

# حسابکردنی Bending Moment
max_moment = (load * length) / 4
st.success(f"بڕی گەورەترین زەبر (Max Bending Moment): {max_moment:.2f} kN.m")

# کێشانی هێڵکاری Bending Moment Diagram (BMD)
x = np.linspace(0, length, 100)
moment = np.where(x <= length/2, (load/2)*x, (load/2)*(length - x))

fig, ax = plt.subplots()
ax.plot(x, moment, color='#1f77b4', linewidth=2.5)
ax.fill_between(x, moment, color='#1f77b4', alpha=0.15)
ax.set_title("Bending Moment Diagram (BMD)", fontsize=14, fontweight='bold')
ax.set_xlabel("Length (m)")
ax.set_ylabel("Moment (kN.m)")
ax.grid(True, linestyle='--', alpha=0.6)
ax.invert_yaxis()  # ڕێکخستنی ئاڕاستەی هەڵگەڕانەوەی BMD

st.pyplot(fig)
