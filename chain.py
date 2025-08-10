import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "dummy"

BASE_URL = "http://localhost:12434/engines/llama.cpp/v1"
MODEL = "ai/gpt-oss:latest"


model = ChatOpenAI(model=MODEL, base_url=BASE_URL)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたはアプリ開発者向けアシスタントです"),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{question}"),
    ]
)

st.set_page_config(page_title="Local Model Chat", page_icon="🤖")
st.title("Local Model Chat (Docker Models)")
st.caption("エンドポイント: " + BASE_URL + " / モデル: " + MODEL)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for m in st.session_state["chat_history"]:
    role = "user" if isinstance(m, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(m.content)

user_input = st.chat_input("メッセージを入力")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    chain = prompt | model | StrOutputParser()

    with st.chat_message("assistant"):
        placehoder = st.empty()
        full_text = ""
        for chunk in chain.stream(
            {"chat_history": st.session_state["chat_history"], "question": user_input}
        ):
            full_text += chunk
            placehoder.markdown(full_text)

    st.session_state["chat_history"].extend(
        [HumanMessage(content=user_input), AIMessage(content=full_text)]
    )
