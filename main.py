import streamlit as st
import cohere
import os

# Cohere APIキー（Secretsから取得）
co = cohere.Client(os.getenv("COHERE_API_KEY"))

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
あなたはフラクタル心理学に基づくカウンセラーです。
以下の対人トラブルについて、日本語で300文字以内のカウンセリングコメントを書いてください。

・自己投影や観念の視点から分析してください
・その観念がどのように過去の思い込みから生まれているか指摘してください
・観念を変えることでどう現実が変わるか優しく提案してください

【トラブル内容】
{user_event}
"""

        response = co.generate(
            model="command",
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )

        ai_comment = response.generations[0].text.strip()

        st.subheader("🧠 AIからの気づき")
        st.markdown(ai_comment)
