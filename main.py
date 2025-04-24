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
あなたは、フラクタル心理学に基づくカウンセラーです。
以下の「対人トラブル」に対し、以下の3ステップでコメントしてください。

1. 【分析】：相手に感じた不快感の背景にある「自分の観念」や「自己投影」について考察してください。
2. 【気づき】：その観念がどのような過去の体験や思い込みに基づいているのか気づかせてください。
3. 【提案】：その観念をどう書き換えれば、現実が好転するか提案してください。

※回答は日本語で、専門的かつ温かい口調で、300文字程度でお願いします。

【対人トラブルの内容】
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
