# zenn-x-post

Zennの記事投稿を自動でX（Twitter）に投稿するGitHub Actions

## 概要

このリポジトリは、Zennの記事管理リポジトリで新しい記事が投稿された際に、自動的にX（Twitter）に投稿するためのGitHub Actionsを提供します。

## 機能

- 新規記事の自動検出
- OpenAI APIを使用したAI生成リード文
- X（Twitter）への自動投稿

## 使用方法

### 1. リポジトリのセットアップ

```bash
git clone https://github.com/kannna5296/zenn-x-post.git
cd zenn-x-post
```

### 2. 必要なシークレットの設定

GitHubリポジトリのSettings > Secrets and variables > Actionsで以下のシークレットを設定してください：

- `OPENAI_API_KEY`: OpenAI APIキー
- `TWITTER_API_KEY`: Twitter APIキー
- `TWITTER_API_SECRET`: Twitter APIシークレット
- `TWITTER_ACCESS_TOKEN`: Twitterアクセストークン
- `TWITTER_ACCESS_SECRET`: Twitterアクセスシークレット

### 3. 他のリポジトリでの使用

Zennの記事管理リポジトリの`.github/workflows/`に以下のワークフローファイルを作成：

```yaml
name: Post to X with AI

on:
  push:
    branches:
      - main
    paths:
      - 'articles/**/*.md'
      - 'books/**/*.md'

jobs:
  post-to-x:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Post to X with AI
        uses: kannna5296/zenn-x-post@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          twitter_api_key: ${{ secrets.TWITTER_API_KEY }}
          twitter_api_secret: ${{ secrets.TWITTER_API_SECRET }}
          twitter_access_token: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          twitter_access_secret: ${{ secrets.TWITTER_ACCESS_SECRET }}
```

## ライセンス

MIT License 