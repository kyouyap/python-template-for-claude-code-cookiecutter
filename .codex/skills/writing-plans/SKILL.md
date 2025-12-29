---
name: writing-plans
description: 複数ステップのタスクに対する仕様や要件があり、コードに触れる前に使用する
---

# 計画を書く

## 概要

エンジニアがコードベースの文脈をほぼ持たず、趣味も怪しい前提で、包括的な実装計画を書く。各タスクで触るファイル、コード、テスト、参照すべきドキュメント、テスト方法など、必要な情報をすべて記載する。計画全体は一口サイズのタスクに分ける。DRY。YAGNI。TDD。こまめなコミット。

熟練開発者だが、ツールセットや問題領域の理解はほぼない前提。良いテスト設計もあまり分かっていない前提。

**開始時に宣言:** 「writing-plans の skill を使って実装計画を作成します。」

**コンテキスト:** 専用の worktree で実行すること (brainstorming の skill で作成)。

**計画の保存先:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 一口サイズのタスク粒度

**各ステップは 1 つの行動 (2〜5 分):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## 計画ドキュメントのヘッダー

**すべての計画はこのヘッダーで始めること:**

```markdown
# [Feature Name] 実装計画

> **Claude 向け:** 必須サブスキル: superpowers:executing-plans を使ってこの計画をタスク単位で実行すること。

**Goal:** [何を構築するか 1 文で記述]

**Architecture:** [アプローチを 2〜3 文で記述]

**Tech Stack:** [主要な技術/ライブラリ]

---
```

## タスク構成

```markdown
### タスク N: [コンポーネント名]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**ステップ 1: 失敗するテストを書く**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**ステップ 2: テストを実行して失敗を確認**

Run: `pytest tests/path/test.py::test_name -v`
Expected: "function not defined" で FAIL

**ステップ 3: 最小実装を書く**

```python
def function(input):
    return expected
```

**ステップ 4: テストを実行して成功を確認**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**ステップ 5: コミット**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 覚えておくこと
- 常に正確なファイルパス
- 計画内に完全なコードを書く ("validation を追加" ではない)
- 期待出力を含む正確なコマンド
- 関連 skills を @ 構文で参照
- DRY、YAGNI、TDD、こまめなコミット

## 実行の引き渡し

計画を保存した後、実行方法の選択肢を提示する:

**「計画は完了し、`docs/plans/<filename>.md` に保存しました。実行方法は 2 つです:」**

**1. Subagent-Driven (このセッション)** - タスクごとに新しいサブエージェントを割り当て、タスク間でレビュー、素早く反復

**2. Parallel Session (別セッション)** - executing-plans で新しいセッションを開き、チェックポイント付きでバッチ実行

**「どちらにしますか?」**

**Subagent-Driven を選んだ場合:**
- **必須サブスキル:** superpowers:subagent-driven-development を使用
- このセッションに留まる
- タスクごとに新しいサブエージェント + コードレビュー

**Parallel Session を選んだ場合:**
- worktree で新しいセッションを開くよう案内
- **必須サブスキル:** 新しいセッションで superpowers:executing-plans を使用
