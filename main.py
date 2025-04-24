import streamlit as st
import os
import re

st.set_page_config(page_title="フラクタル心理診断（日本語版）", page_icon="🧠")
st.title("🧠 フラクタル心理診断 with 日本語共感コメント + 観念補完")
st.markdown("""
以下のフォームに、あなたが最近感じた「対人トラブル」を日本語で記入してください。
AIが日本語で診断コメントを生成し、「承認欲求」に関する観念補完も自動で行います。
""")

# 承認欲求観念辞書（キーワード→自動補完）
belief_patterns = {
    "承認欲求": {
        "keywords": ["無視", "認められない", "評価", "伝わらない", "疎外", "軽視", "過小評価", "意見が通らない", "反論された", "聞いてもらえない"],
        "message": "この出来事には、「私は認められるべきだ」という観念が関係しているかもしれません。相手の態度や言動に強く反応した背景には、“自分の価値が受け入れられていないのでは”という不安が潜んでいた可能性があります。\nフラクタル心理学では、外の世界は内面の鏡です。この体験は、あなたが“自分で自分を認める力”を育てるための大切な気づきになるかもしれません。"
    }
}

with st.form("diagnosis_form"):
    user_event = st.text_area("🔍 最近起こったトラブル内容を記入してください（日本語）", height=200)
    submitted = st.form_submit_button("🧠 診断する")

if submitted:
    with st.spinner("共感的なAI診断を生成中です…"):

        # ナチュラルな共感コメントテンプレートに基づく出力（手動模擬）
        base_comment = f"""
あなたは最近、「{user_event[:30]}…」という出来事の中で、きっと不安や戸惑い、そして悔しさを感じられたのではないでしょうか。
そのように心を動かされた背景には、あなた自身が大切にしている価値観や、“こうありたい”という思いがあったからこそ。

この出来事は、あなたが自分自身と深く向き合うきっかけになるかもしれません。
"""

        # 観念補完の判定と適用
        belief_message = ""
        content = belief_patterns["承認欲求"]
        if any(keyword in user_event for keyword in content["keywords"]):
            belief_message = content["message"]

        final_output = base_comment + "\n\n🔍 フラクタル心理学的観点からの補足:\n" + belief_message if belief_message else base_comment

        st.subheader("🧠 AIからの気づき（日本語診断＋観念補完）")
        st.markdown(final_output)
