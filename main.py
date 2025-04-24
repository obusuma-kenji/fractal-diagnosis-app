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
あなたは、フラクタル心理学に精通したカウンセラーです。

以下の「対人トラブル」について、以下の3つの観点から、
**日本語で、優しく断定的な口調で**コメントしてください。

1. 相手に感じた不快感の背景にある「自分の観念」や「自己投影」
2. 自分の中にある思い込みや過去のパターンに気づかせる
3. 今後どう観念を変えれば現実が変わるかの提案

【トラブル内容】
{user_event}
"""

        response = co.generate(
            model="command-light",
            prompt=prompt,
            max_tokens=500,
            temperature=0.6
        )

        ai_comment = response.generations[0].text.strip()

        st.subheader("🧠 AIからの気づき")
        st.markdown(ai_comment)
