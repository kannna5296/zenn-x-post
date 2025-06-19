# zenn-x-post リポジトリセットアップ手順

## 1. GitHubリポジトリの作成

1. GitHubで新しいリポジトリ `zenn-x-post` を作成
2. リポジトリを公開（Public）に設定
3. このディレクトリの内容をリポジトリにプッシュ

## 2. リポジトリの初期化

```bash
cd zenn-x-post-repo
git init
git add .
git commit -m "Initial commit: Zenn X Post Action"
git branch -M main
git remote add origin https://github.com/kannna5296/zenn-x-post.git
git push -u origin main
```

## 3. GitHub Actionsの有効化

1. GitHubリポジトリのSettings > Actions > General
2. "Allow all actions and reusable workflows" を選択
3. "Allow GitHub Actions to create and approve pull requests" にチェック

## 4. 動作確認

元のZennリポジトリで新しい記事を投稿して、X投稿が正常に動作することを確認してください。

## 5. トラブルシューティング

### アクションが見つからない場合

- リポジトリが公開されていることを確認
- ブランチ名が `main` であることを確認
- アクションの呼び出しパスが正しいことを確認

### シークレットエラー

- 元のリポジトリに必要なシークレットが設定されていることを確認
- シークレット名が正しいことを確認

## 6. 更新手順

アクションを更新する場合：

1. このディレクトリでファイルを編集
2. コミットしてプッシュ
3. 元のリポジトリで新しい記事を投稿してテスト 