#!/usr/bin/env python3
import sys
import os
import json
import requests

PREFIX = "[generate-ai-lead.py]"
DEFAULT_MESSAGE = "📝 新しい技術記事を投稿しました！"

def log(msg):
    print(f"{PREFIX} {msg}")

def set_output(name, value):
    # 改行や%などをエスケープ
    value = value.replace('%', '%25').replace('\n', '%0A').replace('\r', '%0D')
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
        f.write(f"{name}={value}\n")

if len(sys.argv) != 3:
    print(f"{PREFIX} Usage: generate-ai-lead.py <article_title> <article_url> <openai_api_key>")
    sys.exit(1)

ARTICLE_TITLE = sys.argv[1]
ARTICLE_URL = sys.argv[2]
OPENAI_API_KEY = sys.argv[3]
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", None)
if not GITHUB_OUTPUT:
    print(f"{PREFIX} GITHUB_OUTPUT env not set. Exiting.")
    sys.exit(1)

AI_LEAD = None

if OPENAI_API_KEY:
    log("=== OpenAI API Request ===")
    log(f"Article URL: {ARTICLE_URL}")
    log(f"OpenAI API Key: {OPENAI_API_KEY[:10]}...")

    system_content = "あなたは技術記事のプロモーション専門家です。指定されたURLの記事を読み取って、Xで人々がクリックしたくなる魅力的なリード文を生成してください。要件: 90文字以内。技術的な価値を強調、読者の興味を引く表現、ハッシュタグは含めない、記事の具体的なメリットを明示。"
    user_content = f"以下のURLの技術記事を読み取って、X投稿用の魅力的なリード文を生成してください：\n\n{ARTICLE_URL}"

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    log("Request JSON:")
    log(json.dumps(payload, ensure_ascii=False, indent=2))

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        http_status = response.status_code
        response_body = response.text
    except Exception as e:
        log(f"❌ OpenAI API request failed: {e}")
        http_status = None
        response_body = ""

    log(f"HTTP Status Code: {http_status}")
    log("Response Body:")
    print(response_body)
    log("")

    if http_status == 200:
        try:
            data = response.json()
            lead = data["choices"][0]["message"]["content"].strip()
            if lead:
                AI_LEAD = lead.replace('\n', '').strip('"')
                log("✅ Successfully generated AI lead text")
            else:
                log("❌ No content found in OpenAI response")
        except Exception as e:
            log(f"❌ Failed to parse JSON response: {e}")
            log(f"Raw response: {response_body}")
    else:
        log(f"❌ OpenAI API request failed with status: {http_status}")
        log(f"Error response: {response_body}")
else:
    log("OpenAI APIキー未指定のため、AIリード文生成をスキップします")

# 投稿文の組み立て
if AI_LEAD:
    POST_MESSAGE = f"{DEFAULT_MESSAGE}\n\n{AI_LEAD}\n\n{ARTICLE_URL}"
else:
    POST_MESSAGE = f"{DEFAULT_MESSAGE}\n\n{ARTICLE_URL}"

log(f"Final post message: {POST_MESSAGE}")
set_output("post_message", POST_MESSAGE) 