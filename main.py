import streamlit as st
import cohere
import os
from googletrans import Translator

# Cohere APIキー（Secretsから取得）
co = cohere.Client(os.getenv("COHERE_API_KEY"))
translator = Translator()

st.set_page_config(page_title="フラクタル心理診断 with 翻訳対応", page_icon="🧠")
st.title("🧠 フラクタル心理診断 with 英語生成＋日本語翻訳")
st.markdown("""
以下のフォームに、あなたが最近感じた「対人トラブル」を記入してください。
英語でAIが分析を行い、日本語で結果が表示されます。
""")

with st.form("diagnosis_form"):
    user_event = st.text_area("🔍 最近起こったトラブル内容を記入してください", height=150)
    submitted = st.form_submit_button("🧠 診断する")

if submitted:
    with st.spinner("AIカウンセラーが診断中です..."):
        prompt = f"""
You are a counselor trained in Fractal Psychology.

Please respond to the following interpersonal conflict in English, following these three steps:

1. Description: Briefly describe what happened.
2. Reflection: How did the client feel about it, and what was their internal emotional reaction?
3. Fractal Insight & Suggestion: From a Fractal Psychology perspective, what unconscious patterns, projections, or inner beliefs does this event reflect? What growth or healing opportunity is available to the client?

Respond in a warm, empathic, and professional tone, in 300–500 characters.

Here is the event:
{user_event}
"""

        response = co.generate(
            model="command",
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )

        english_comment = response.generations[0].text.strip()
        translated_comment = translator.translate(english_comment, src='en', dest='ja').text

        st.subheader("🧠 AIからの気づき（日本語訳）")
        st.markdown(translated_comment)

        with st.expander("📝 英語の原文も確認する"):
            st.markdown(english_comment)
