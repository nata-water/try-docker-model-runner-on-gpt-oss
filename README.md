## 前提

- Docker Desktop がインストールされていること
- Docker Model Runner が有効になっていること
  - Settings -> Beta features -> Enable Docker Model Runner にチェックを入れる
  - Enable host-side TCP support にチェックを入れる
  - （GPU あれば）Enable GPU-backed-inference にチェックを入れる

## 必要なモデル及びツールのインストール

```shell
# モデルのPull
docker model pull ai/gpt-oss:latest

# uvのインストール
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## パッケージ同期及び実行

```shell
uv sync
uv run streamlit run main.py

```


## 実行後

- モデルのアンロード
  - これを実行しないと、GPUメモリが解放されないため、要注意

```shell
docker model unload ai/gpt-oss:latest
```
