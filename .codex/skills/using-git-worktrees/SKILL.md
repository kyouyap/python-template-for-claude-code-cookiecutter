---
name: using-git-worktrees
description: Use when 現在のワークスペースから分離が必要な機能開発を始めるとき、または実装計画を実行する前に使う。安全確認と賢いディレクトリ選択を伴う git worktree を作成する。
---

# Git Worktree の使い方

## 概要

Git worktree は同じリポジトリを共有する独立作業領域を作り、ブランチを切り替えずに同時進行を可能にする。

**中核原則:** 系統立てたディレクトリ選択 + 安全確認 = 信頼できる分離。

**開始時に宣言:** "using-git-worktrees スキルを使って隔離されたワークスペースを作成します。"

## ディレクトリ選択プロセス

以下の優先順位に従う:

### 1. 既存ディレクトリの確認

```bash
# 優先順で確認
ls -d .worktrees 2>/dev/null     # 推奨（隠し）
ls -d worktrees 2>/dev/null      # 代替
```

**見つかった場合:** そのディレクトリを使う。両方あるなら `.worktrees` を優先。

### 2. CLAUDE.md の確認

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**設定がある場合:** その指定に従い、質問せずに使う。

### 3. ユーザーに質問

ディレクトリが存在せず、CLAUDE.md に指定もない場合:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全確認

### プロジェクトローカル（.worktrees / worktrees）の場合

**作成前に必ず ignore 済みか確認:**

```bash
# ignore されているか確認（ローカル/グローバル/システムの gitignore を尊重）
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**ignore されていない場合:**

Jesse のルール "Fix broken things immediately" に従う:
1. .gitignore に適切な行を追加
2. 変更をコミット
3. worktree 作成を続行

**重要理由:** worktree の内容がリポジトリに誤ってコミットされるのを防ぐ。

### グローバルディレクトリ（~/.config/superpowers/worktrees）の場合

プロジェクト外なので .gitignore の確認は不要。

## 作成手順

### 1. プロジェクト名の検出

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. worktree の作成

```bash
# フルパスを決定
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# 新しいブランチで worktree 作成
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. プロジェクトセットアップ

自動検出して適切なセットアップを実行:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. クリーンなベースライン確認

worktree がクリーンに始まるかテストで確認:

```bash
# 例 - プロジェクトに合わせる
npm test
cargo test
pytest
go test ./...
```

**テストが失敗:** 失敗を報告し、続行か調査かを質問。

**テストが成功:** 準備完了を報告。

### 5. 場所の報告

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## クイックリファレンス

| 状況 | 対応 |
|-----------|--------|
| `.worktrees/` がある | それを使う（ignore 確認） |
| `worktrees/` がある | それを使う（ignore 確認） |
| 両方ある | `.worktrees/` を使う |
| どちらもない | CLAUDE.md → ユーザーに質問 |
| ディレクトリが ignore されていない | .gitignore に追加 + コミット |
| ベースラインでテスト失敗 | 失敗を報告 + 質問 |
| package.json/Cargo.toml なし | 依存インストールをスキップ |

## よくあるミス

### ignore 確認の省略

- **問題:** worktree の内容が追跡され、git status が汚れる
- **修正:** プロジェクトローカルでは必ず `git check-ignore` を実行

### ディレクトリ場所を決め打ち

- **問題:** 一貫性が崩れ、プロジェクト規約に違反
- **修正:** 既存 > CLAUDE.md > 質問 の優先順を守る

### テスト失敗のまま進行

- **問題:** 新規バグと既存問題の区別ができない
- **修正:** 失敗を報告し、明示的な許可を得る

### セットアップコマンドの固定化

- **問題:** ツールが異なるプロジェクトで壊れる
- **修正:** プロジェクトファイルから自動検出（package.json など）

## 例ワークフロー

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## レッドフラグ

**決してやらない:**
- ignore 確認なしに worktree を作成（プロジェクトローカル）
- ベースラインテストの確認を省略
- テスト失敗のまま質問せず続行
- ディレクトリ場所を曖昧なまま決める
- CLAUDE.md の確認を省略

**必ずやる:**
- 優先順を守る: 既存 > CLAUDE.md > 質問
- プロジェクトローカルでは ignore 済みを確認
- セットアップを自動検出して実行
- クリーンなテストベースラインを確認

## 統合

**呼び出し元:**
- **brainstorming**（Phase 4）- 設計承認後の実装開始時に必須
- 隔離ワークスペースが必要なスキル

**組み合わせ:**
- **finishing-a-development-branch** - 完了後のクリーンアップで必須
- **executing-plans** / **subagent-driven-development** - 作業はこの worktree 内で行う
