import streamlit as st
from openai import OpenAI

# Docker Models (Docker Desktop) のローカルOpenAI互換エンドポイント
BASE_URL = "http://localhost:12434/engines/llama.cpp/v1"
MODEL = "ai/gpt-oss:latest"

st.set_page_config(page_title="Local Model Chat", page_icon="🤖")
st.title("gpt-oss Local Model Chat (Docker Model Runner)")
st.caption("エンドポイント: " + BASE_URL + " / モデル: " + MODEL)

# OpenAI クライアント初期化
# Docker Models はAPIキー不要だが、openai>=1系は値が必須のためダミーを設定
client = OpenAI(base_url=BASE_URL, api_key="dummy")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "あなたはアプリ開発者のサポートに特化したアシスタントです",
        }
    ]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.write(m["content"])

prompt = st.chat_input("メッセージを入力...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ("system", "user", "assistant")
            ],
            stream=True,
        )
        with st.chat_message("assistant"):

            def stream_tokens():
                for chunk in res:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta
                    content = getattr(delta, "content", None)
                    if content:
                        yield content

            full_text = st.write_stream(stream_tokens)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_text}
            )

    except Exception as e:
        st.error(
            "モデル呼び出しに失敗しました。Docker DesktopのDocker Models機能が有効か、モデルが取得済みかをご確認ください。"
        )
        st.exception(e)
