import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import cohere

# フォント存在確認付き
font_path = os.path.join(os.path.dirname(__file__), "fonts", "NotoSansJP-Regular.ttf")
font_prop = fm.FontProperties(fname=font_path) if os.path.isfile(font_path) else None

co = cohere.Client(os.getenv("COHERE_API_KEY"))

st.set_page_config(page_title="フラクタル診断", page_icon="🧠")
st.title("🧠 フラクタル心理診断 with 日本語フォント")

with st.form("diagnosis_form"):
    user_event = st.text_area("📌 最近の対人トラブルについて教えてください", height=150)
    user_feeling = st.text_area("💭 そのときの気持ちを教えてください", height=100)
    submitted = st.form_submit_button("診断する")

if submitted:
    with st.spinner("診断中..."):
        prompt = f"""
あなたが最近経験した対人トラブル：
{user_event}

あなたの感情：
{user_feeling}

この出来事をフラクタル心理学の視点から見た場合、どのような潜在意識が関係していると考えられるでしょうか？
日本語で優しく、深い気づきを与えるアドバイスを生成してください。
"""
        try:
            response = co.generate(model="command-r", prompt=prompt, max_tokens=500)
            st.success("診断が完了しました！")
            st.markdown("### 🧠 AIからの気づき")
            st.markdown(response.generations[0].text.strip())

            # グラフ描画（フォントあり／なし）
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [2, 3, 1])
            ax.set_title("感情の変化グラフ", fontproperties=font_prop)
            ax.set_xlabel("時間", fontproperties=font_prop)
            ax.set_ylabel("強度", fontproperties=font_prop)
            st.pyplot(fig)

        except Exception as e:
            st.error("診断中にエラーが発生しました")
            st.text(str(e))
