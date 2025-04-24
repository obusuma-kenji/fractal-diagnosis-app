import streamlit as st
import cohere
import os
from googletrans import Translator
import re

# 観念分類表（初期構成）
belief_patterns = {
    "承認欲求": {
        "keywords": ["無視", "認められない", "評価", "伝わらない", "疎外"],
        "message": "今回の出来事には、「私は認められるべきだ」という観念が背景にある可能性があります。相手の反応は、あなたが自分の価値を外からの評価に依存しているパターンを映しているかもしれません。"
    },
    "完璧主義": {
        "keywords": ["ミス", "指摘", "責められた", "失敗", "恥ずかしい"],
        "message": "この体験からは、「私は間違えてはいけない」という完璧主義の観念が見えてきます。自分のミスに過度に反応する傾向が、相手の態度に敏感に反応してしまったのかもしれません。"
    },
    "コントロール欲": {
        "keywords": ["従わない", "勝手", "予定変更", "混乱", "無計画"],
        "message": "今回のような状況には、「私は思い通りに進めたい」というコントロール欲の観念が関わっている可能性があります。状況が自分の枠を外れたとき、強い不快感として現れることがあります。"
    }
}

# Cohere APIキー（Secretsから取得）
co = cohere.Client(os.getenv("COHERE_API_KEY"))
translator = Translator()

st.set_page_config(page_title="フラクタル心理診断 with 翻訳＆観念補完", page_icon="🧠")
st.title("🧠 フラクタル心理診断")
st.markdown("""
以下のフォームに、あなたが最近感じた「対人トラブル」を記入してください。
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

        # ナチュラライズ変換辞書
        replacements = {
            "クライアント": "あなた",
            "検討する必要があります": "してみると良いでしょう",
            "認識することができます": "と捉えることもできそうです",
            "する必要があります": "すると良いでしょう",
            "オープンなコミュニケーションライン": "率直に気持ちを伝え合う場",
            "と感じている場合": "と感じることがあるならば",
            "同僚": "相手",
            "によって動機付けられています": "という気持ちが根底にあるようです",
            "として使用し": "と捉えて",
            "。": "。\n"
        }

        modified_comment = translated_comment
        for key, value in replacements.items():
            modified_comment = re.sub(key, value, modified_comment)

        # 観念自動補完の挿入
        belief_message = ""
        for belief, content in belief_patterns.items():
            if any(keyword in user_event for keyword in content["keywords"]):
                belief_message = content["message"]
                break

        final_output = modified_comment + "\n\n🔍 フラクタル心理学的観点からの補足:\n" + belief_message if belief_message else modified_comment

        st.subheader("🧠 AIからの気づき（日本語訳）")
        st.markdown(final_output)

        with st.expander("📝 英語の原文も確認する"):
            st.markdown(english_comment)
