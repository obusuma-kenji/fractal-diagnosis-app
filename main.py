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
あなたはフラクタル心理学の専門家です。
以下の「対人トラブル」について、次の3ステップに従い、日本語で温かく断定的に回答してください。

【分析】：相手に感じた不快感の背後にある「自分の観念」や「自己投影」を解説。
【気づき】：その観念が過去のどのような体験や思い込みに基づいているのか指摘。
【提案】：その観念をどう変えれば現実が好転するか、実践的な提案を。

【対人トラブル】
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
