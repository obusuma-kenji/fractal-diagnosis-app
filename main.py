import streamlit as st
import os
import re

st.set_page_config(page_title="フラクタル心理診断（日本語・2段階入力版）", page_icon="🧠")
st.title("🧠 フラクタル心理診断 〜 自分の観念に気づく対話体験")
st.markdown("""
以下の2つの質問に答えることで、あなたの内面にある観念のパターンが浮かび上がります。
すべて日本語で入力してください。
""")

# 観念分類表（簡易）
kannen_table = {
    "無視": "私は大切にされないという観念",
    "イライラ": "思い通りにいかないと不安になるという観念",
    "悲しみ": "自分の価値が他人に左右されるという観念",
    "不安": "失敗したら愛されないという観念",
    "評価されない": "結果を出せないと認められないという観念"
}

# 感情文から観念を補完する

def supplement_kannen(feeling_text):
    supplemented = []
    for keyword, kannen in kannen_table.items():
        if keyword in feeling_text:
            supplemented.append(kannen)
    return supplemented

# 診断コメント生成
def generate_diagnosis(trouble, feeling):
    empathy = f"あなたが感じた『{feeling}』という感情は、とても自然なものです。"
    kannen_list = supplement_kannen(feeling)

    if kannen_list:
        insight = "この出来事を通じて見えてくる観念には、以下のようなものがあるかもしれません：\n"
        for k in kannen_list:
            insight += f"- {k}\n"
    else:
        insight = "今回の感情には、あなた独自の価値観や経験が反応しているかもしれません。"

    closing = "この出来事は、あなたが自分の内面にある観念に気づき、\n自分自身をより深く理解するきっかけになるかもしれません。"

    return f"🧠 AIからの気づき（日本語訳）\n\n{empathy}\n\n{insight}\n\n{closing}"

# フォーム入力
with st.form("2step_form"):
    trouble = st.text_area("① 最近起こったトラブル内容を記入してください", height=150)
    feeling = st.text_area("② その時の気持ちを教えてください", height=150)
    submitted = st.form_submit_button("🧠 診断する")

if submitted:
    with st.spinner("診断中です…"):
        result = generate_diagnosis(trouble, feeling)
        st.subheader("📝 診断結果")
        st.markdown(result)
