import streamlit as st
import cohere
import os
from matplotlib import pyplot as plt
from matplotlib import font_manager
import numpy as np

# Cohere APIキー（Secretsから取得）
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# 日本語フォント設定
font_path = os.path.join(os.path.dirname(__file__), "NotoSansJP-Regular.ttf")
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

st.set_page_config(page_title="フラクタル心理診断 with 日本語フォント対応", page_icon="🧠")
st.title("🧠 フラクタル心理診断 with 日本語フォント対応")
st.markdown("""
以下のフォームに、あなたが最近感じた「対人トラブル」を記入してください。
""")

with st.form("diagnosis_form"):
    user_event = st.text_area("🔍 最近起こったトラブル内容を記入してください", height=150)
    submitted = st.form_submit_button("🧠 診断する")

if submitted:
    with st.spinner("AIカウンセラーが診断中です..."):
        prompt = f"""
あなたはフラクタル心理学に基づくプロフェッショナルなカウンセラーです。
以下の「対人トラブル」について、次の構成に従ってコメントをください：

1. 【分析】相手に感じた感情の背後にある「自分の観念」や「自己投影」
2. 【気づき】自分の中にある思い込み・過去の経験の反映
3. 【提案】今後どう思考を修正すれば、よりよい関係や現実が得られるか

敬語で、やさしく、クライアントの成長を応援する語り口でお願いします。

【トラブル内容】
{user_event}
"""

        response = co.generate(
            model="command",
            prompt=prompt,
            max_tokens=300,
            temperature=0.65
        )

        ai_comment = response.generations[0].text.strip()

        st.subheader("🧠 AIからの気づき")
        st.markdown(ai_comment)

        # 感情バランス仮想推移図
        st.subheader("📊 感情バランスの仮想推移")
        fig, ax = plt.subplots()
        x = np.arange(1, 4)
        y = [1.8, 3.0, 2.2]  # サンプル数値
        ax.plot(x, y, marker='o')
        ax.set_title("感情バランスの仮想推移", fontproperties=font_prop)
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels(["不安", "怒り", "自己否定"], fontproperties=font_prop)
        ax.set_ylabel("強さ (1~5)", fontproperties=font_prop)
        st.pyplot(fig)

