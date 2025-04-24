import streamlit as st
import os
import re

st.set_page_config(page_title="フラクタル心理診断（観念拡張版）", page_icon="🧠")
st.title("🧠 フラクタル心理診断 〜 自分の観念に気づく対話体験")
st.markdown("""
以下の2つの質問に答えることで、あなたの内面にある観念のパターンが浮かび上がります。
すべて日本語で入力してください。
""")

# 拡張版 観念分類辞書
def get_kannen_table():
    return {
        "無視": "私は大切にされないという観念",
        "イライラ": "思い通りにいかないと不安になるという観念",
        "焦り": "早く結果を出さないと認められないという観念",
        "恥ずかしさ": "失敗＝価値がないという思い込み",
        "怒り": "自分はもっと尊重されるべきという観念",
        "悲しみ": "人にわかってもらえない寂しさという観念",
        "不安": "相手に合わせないと嫌われるかもしれないという観念",
        "悔しさ": "自分の実力が正当に評価されていないという観念",
        "孤独": "どうせ一人では何もできないという無意識の思い",
        "安心": "コントロールできる環境だけが安全という観念",
        "あきらめ": "自分の努力はどうせ報われないという信念"
    }

# 感情文から観念を補完する

def supplement_kannen(feeling_text):
    supplemented = []
    for keyword, kannen in get_kannen_table().items():
        if keyword in feeling_text:
            supplemented.append(kannen)
    return supplemented

# 診断コメント生成
def generate_diagnosis(trouble, feeling):
    empathy = f"あなたが感じた『{feeling}』という感情は、とても自然なものです。"
    kannen_list = supplement_kannen(feeling)

    if kannen_list:
        insight = "\n\nこの出来事を通じて見えてくる観念には、以下のようなものがあるかもしれません：\n"
        for k in kannen_list:
            insight += f"- {k}\n"
        closing = "\nこれらの観念は、これまでの経験や思い込みから生まれてきたかもしれません。\n気づいた今こそ、自分をもっと自由にしていくチャンスです。"
    else:
        insight = "\n\n今回の感情には、あなた独自の価値観や過去の経験が強く影響しているかもしれません。"
        closing = "\nこの気づきから、新たな行動や思考の選択が生まれる可能性があります。"

    return f"🧠 AIからの気づき（日本語訳）\n\n{empathy}{insight}{closing}"

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
