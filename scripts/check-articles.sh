#!/bin/bash

# 記事の公開状態をチェックするスクリプト
# 使用方法: ./check-articles.sh <new_files> <modified_files>

PREFIX="[check-articles.sh]"

NEW_FILES="$1"
MODIFIED_FILES="$2"

SHOULD_POST="false"
ARTICLE_TITLE=""
ARTICLE_URL=""

log() {
  echo "$PREFIX $1"
}

# 新規ファイルがある場合
if [ -n "$NEW_FILES" ]; then
  FILE_PATH="$NEW_FILES"
  log "Checking new file: $FILE_PATH"
  
  # published: true が含まれているかチェック
  if grep -q "published: true" "$FILE_PATH"; then
    log "New published article found: $FILE_PATH"
    SHOULD_POST="true"
    
    # ファイルの最初の行からタイトルを取得（# で始まる場合）
    FIRST_LINE=$(head -n 1 "$FILE_PATH" | sed 's/^# //')
    if [[ "$FIRST_LINE" == \#* ]]; then
      ARTICLE_TITLE="$FIRST_LINE"
    else
      # ファイル名からタイトルを抽出（拡張子と日付を除去）
      FILENAME=$(basename "$FILE_PATH" .md)
      ARTICLE_TITLE=$(echo "$FILENAME" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//' | sed 's/-/ /g')
    fi
    
    # ZennのURLを生成
    # TODO アカウントIDは外から注入できるようにする
    # TODO Zenn以外も対応するハテナとかもいけそう？
    if [[ "$FILE_PATH" == articles/* ]]; then
      SLUG=$(basename "$FILE_PATH" .md)
      ARTICLE_URL="https://zenn.dev/kannna5296/articles/${SLUG}"
    elif [[ "$FILE_PATH" == books/* ]]; then
      SLUG=$(basename "$FILE_PATH" .md)
      ARTICLE_URL="https://zenn.dev/kannna5296/books/${SLUG}"
    fi
  else
    log "New file is not published: $FILE_PATH"
  fi
  
# 変更されたファイルがある場合
elif [ -n "$MODIFIED_FILES" ]; then
  FILE_PATH="$MODIFIED_FILES"
  log "Checking modified file: $FILE_PATH"
  
  # 変更前のファイルのpublished状態を確認
  PREV_PUBLISHED=false
  if git show HEAD~1:"$FILE_PATH" 2>/dev/null | grep -q "published: true"; then
    PREV_PUBLISHED=true
  fi
  
  # 現在のファイルのpublished状態を確認
  CURRENT_PUBLISHED=false
  if grep -q "published: true" "$FILE_PATH"; then
    CURRENT_PUBLISHED=true
  fi
  
  log "Previous published state: $PREV_PUBLISHED"
  log "Current published state: $CURRENT_PUBLISHED"
  
  # published: false から published: true に変更された場合
  if [ "$PREV_PUBLISHED" = "false" ] && [ "$CURRENT_PUBLISHED" = "true" ]; then
    log "Article published status changed from false to true: $FILE_PATH"
    SHOULD_POST="true"
    
    # ファイルの最初の行からタイトルを取得
    FIRST_LINE=$(head -n 1 "$FILE_PATH" | sed 's/^# //')
    if [[ "$FIRST_LINE" == \#* ]]; then
      ARTICLE_TITLE="$FIRST_LINE"
    else
      # ファイル名からタイトルを抽出
      FILENAME=$(basename "$FILE_PATH" .md)
      ARTICLE_TITLE=$(echo "$FILENAME" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//' | sed 's/-/ /g')
    fi
    
    # ZennのURLを生成
    if [[ "$FILE_PATH" == articles/* ]]; then
      SLUG=$(basename "$FILE_PATH" .md)
      ARTICLE_URL="https://zenn.dev/kannna5296/articles/${SLUG}"
    elif [[ "$FILE_PATH" == books/* ]]; then
      SLUG=$(basename "$FILE_PATH" .md)
      ARTICLE_URL="https://zenn.dev/kannna5296/books/${SLUG}"
    fi
  else
    log "Modified file is not newly published: $FILE_PATH"
  fi
else
  log "No new or modified markdown files found"
fi

# GitHub Actionsの出力形式で結果を出力
echo "should_post=${SHOULD_POST}" >> $GITHUB_OUTPUT
echo "article_title=${ARTICLE_TITLE}" >> $GITHUB_OUTPUT
echo "article_url=${ARTICLE_URL}" >> $GITHUB_OUTPUT 