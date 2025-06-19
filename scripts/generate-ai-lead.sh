#!/bin/bash

# AI Lead生成スクリプト
# 使用方法: ./generate-ai-lead.sh <article_url> <openai_api_key>

PREFIX="[generate-ai-lead.sh]"
log() {
  echo "$PREFIX $1"
}

ARTICLE_URL="$1"
OPENAI_API_KEY="$2"

log "=== OpenAI API Request ==="
log "Article URL: $ARTICLE_URL"
log "OpenAI API Key: ${OPENAI_API_KEY:0:10}..."

# APIリクエストのJSONを作成
cat > request.json << EOF
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "あなたは技術記事のプロモーション専門家です。指定されたURLの記事を読み取って、X（Twitter）で人々がクリックしたくなる魅力的なリード文を生成してください。要件: 90文字以内。技術的な価値を強調、読者の興味を引く表現、ハッシュタグは含めない、記事の具体的なメリットを明示。"
    },
    {
      "role": "user",
      "content": "以下のURLの技術記事を読み取って、X投稿用の魅力的なリード文を生成してください：\n\n$ARTICLE_URL"
    }
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
EOF

log "Request JSON:"
cat request.json
log ""

# OpenAI APIを呼び出し
log "Calling OpenAI API..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @request.json)

# HTTPステータスコードを抽出
HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS:/d')

log "HTTP Status Code: $HTTP_STATUS"
log "Response Body:"
echo "$RESPONSE_BODY"
log ""

# エラーハンドリング
if [ "$HTTP_STATUS" != "200" ]; then
  log "❌ OpenAI API request failed with status: $HTTP_STATUS"
  log "Error response: $RESPONSE_BODY"
  LEAD_TEXT="📝 新しい技術記事を投稿しました！"
else
  # レスポンスからリード文を抽出
  LEAD_TEXT=$(echo "$RESPONSE_BODY" | jq -r '.choices[0].message.content' 2>/dev/null)
  
  # jqのエラーハンドリング
  if [ $? -ne 0 ]; then
    log "❌ Failed to parse JSON response with jq"
    log "Raw response: $RESPONSE_BODY"
    LEAD_TEXT="📝 新しい技術記事を投稿しました！"
  elif [ "$LEAD_TEXT" = "null" ] || [ -z "$LEAD_TEXT" ]; then
    log "❌ No content found in OpenAI response"
    log "Parsed response: $RESPONSE_BODY"
    LEAD_TEXT="📝 新しい技術記事を投稿しました！"
  else
    log "✅ Successfully generated AI lead text"
    LEAD_TEXT=$(echo "$LEAD_TEXT" | tr -d '\n' | sed 's/^"//;s/"$//')
  fi
fi

log "Final lead text: $LEAD_TEXT"
echo "ai_lead_text=${LEAD_TEXT}" >> $GITHUB_OUTPUT 