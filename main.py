import streamlit as st
import cohere
import os
from matplotlib import pyplot as plt
from matplotlib import font_manager
import numpy as np

# Cohere APIキー（Secretsから取得）
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# フォント設定（日本語表示対応）
font_path = os.path.join(os.path.dirname(__file__), "NotoSansJP-Regular.ttf")
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

st.set_page_config(page_title="フラクタル自己診断", page_icon="🧠")
st.title("🧠 フラクタル心理診断 with 日本語フォント対応")
st.markdown("""
以下のフォームに、あなたが最近感じた「対人トラブル」を記入してください。
""")

with st.form("diagnosis_form"):
    user_event = st.text_area("🔍 最近起こったトラブル内容を記入してください", height=150)
    submitted = st.form_submit_button("🧠 診断する")

if submitted:
    st.spinner("AIカウンセラーによる診断中...")

    prompt = f"""
あなたはフラクタル心理学に基づく上級カウンセラーです。

ユーザーが入力した「対人トラブル」に関して、
『他人は自分の鏡である』『この世界は自分が創っている』という一元論の観点から、
以下のような構成で短く、的確にフィードバックをしてください。

1. 【分析】相手に対する感情の背景にある「自己側の観念」や「自己投影」を明らかにする
2. 【気づき】今回の出来事が、どんな思い込みや自己否定から来ていたかを明確にする
3. 【未来志向の提案】今後、自分のどんな言動や観念を変えるとより良くなるかを提案する
4. 【最後に】「これは相手の問題ではなく、すべて自分の観念が創り出した世界である」と明言する

語調は：優しく断定的に（例：「〜と考えられます」「〜することが必要です」）。長すぎず、読みやすく。

【対人トラブル】
{user_event}
"""

    response = co.generate(
        prompt=prompt,
        model="command",  # 正しいモデル指定
        max_tokens=300,
        temperature=0.7
    )

    result = response.generations[0].text

    st.markdown("""
    ## 🧠 AIからの気づき
    """)
    st.write(result)

    # サンプル図（仮の評価値で描画）
    fig, ax = plt.subplots()
    x = np.arange(1, 4)
    y = [2.0, 3.0, 1.5]
    ax.plot(x, y, marker='o')
    ax.set_title("感情バランスの仮想推移", fontproperties=font_prop)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["緊張", "怒り", "不安"], fontproperties=font_prop)
    ax.set_ylabel("強さ (1~5)", fontproperties=font_prop)
    st.pyplot(fig)

