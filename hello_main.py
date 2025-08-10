import os
from openai import OpenAI

# ダミーでOK
os.environ["OPENAI_API_KEY"] = "dummy"

BASE_URL = "http://localhost:12434/engines/llama.cpp/v1"
MODEL = "ai/gpt-oss:latest"

client = OpenAI(base_url=BASE_URL)
res = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "あなたはアプリ開発アシスタントです"},
        {"role": "user", "content": "Dockerについて数行で概要を教えて"},
    ],
)
print(res.choices[0].message.content)
