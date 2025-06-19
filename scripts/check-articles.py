#!/usr/bin/env python3
import sys
import os
import subprocess
import re

PREFIX = "[check-articles.py]"

# 引数: new_file, modified_file
if len(sys.argv) != 3:
    print(f"{PREFIX} Usage: check-articles.py <new_file> <modified_file>")
    sys.exit(1)

NEW_FILE = sys.argv[1]
MODIFIED_FILE = sys.argv[2]

SHOULD_POST = "false"
ARTICLE_TITLE = ""
ARTICLE_URL = ""

GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", None)
if not GITHUB_OUTPUT:
    print(f"{PREFIX} GITHUB_OUTPUT env not set. Exiting.")
    sys.exit(1)

ZENN_USER_ID = os.environ.get("ZENN_USER_ID", None)
if not ZENN_USER_ID:
    print(f"{PREFIX} ZENN_USER_ID env not set. Exiting.")
    sys.exit(1)

def log(msg):
    print(f"{PREFIX} {msg}")

def extract_title(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("# "):
                return first_line[2:]
    except Exception:
        pass
    # ファイル名からタイトル生成
    filename = os.path.basename(file_path)
    filename = re.sub(r"^\\d{4}-\\d{2}-\\d{2}-", "", filename)
    filename = re.sub(r"\\.md$", "", filename)
    return filename.replace("-", " ")

def make_url(file_path):
    if file_path.startswith("articles/"):
        slug = os.path.basename(file_path).replace(".md", "")
        return f"https://zenn.dev/{ZENN_USER_ID}/articles/{slug}"
    elif file_path.startswith("books/"):
        slug = os.path.basename(file_path).replace(".md", "")
        return f"https://zenn.dev/{ZENN_USER_ID}/books/{slug}"
    return ""

def file_contains_published_true(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if "published: true" in line:
                    return True
    except Exception:
        pass
    return False

def git_prev_published_true(file_path):
    try:
        result = subprocess.run([
            "git", "show", f"HEAD~1:{file_path}"
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
        for line in result.stdout.splitlines():
            if "published: true" in line:
                return True
    except Exception:
        pass
    return False

if NEW_FILE:
    file_path = NEW_FILE
    log(f"Checking new file: {file_path}")
    if file_contains_published_true(file_path):
        log(f"New published article found: {file_path}")
        SHOULD_POST = "true"
        ARTICLE_TITLE = extract_title(file_path)
        ARTICLE_URL = make_url(file_path)
    else:
        log(f"New file is not published: {file_path}")
elif MODIFIED_FILE:
    file_path = MODIFIED_FILE
    log(f"Checking modified file: {file_path}")
    prev_published = git_prev_published_true(file_path)
    current_published = file_contains_published_true(file_path)
    log(f"Previous published state: {prev_published}")
    log(f"Current published state: {current_published}")
    if not prev_published and current_published:
        log(f"Article published status changed from false to true: {file_path}")
        SHOULD_POST = "true"
        ARTICLE_TITLE = extract_title(file_path)
        ARTICLE_URL = make_url(file_path)
    else:
        log(f"Modified file is not newly published: {file_path}")
else:
    log("No new or modified markdown files found")

with open(GITHUB_OUTPUT, "a", encoding="utf-8") as f:
    f.write(f"should_post={SHOULD_POST}\n")
    f.write(f"article_title={ARTICLE_TITLE}\n")
    f.write(f"article_url={ARTICLE_URL}\n") 