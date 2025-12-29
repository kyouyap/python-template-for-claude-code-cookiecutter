---
name: requesting-code-review
description: タスク完了時、主要機能の実装時、またはマージ前に、作業が要件を満たしているか検証するために使用する
---

# コードレビューの依頼

superpowers:code-reviewer のサブエージェントをディスパッチし、問題が連鎖する前に捕捉する。

**中核原則:** 早めにレビュー、頻繁にレビュー。

## レビュー依頼のタイミング

**必須:**
- subagent-driven-development の各タスク後
- 主要機能の完了後
- main へマージする前

**任意だが有益:**
- 行き詰まったとき (新しい視点)
- リファクタ前 (ベースライン確認)
- 複雑なバグ修正後

## 依頼方法

**1. git SHA を取得:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. code-reviewer サブエージェントをディスパッチ:**

Task ツールで superpowers:code-reviewer を使い、`code-reviewer.md` のテンプレートを埋める

**プレースホルダー:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. フィードバックに対応:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## 例

```
[タスク 2 完了: 検証関数の追加]

You: 続行前にコードレビューを依頼します。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[superpowers:code-reviewer サブエージェントをディスパッチ]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[サブエージェントの返答]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [進捗インジケータを修正]
[タスク 3 に進む]
```

## ワークフローとの統合

**Subagent-Driven Development:**
- 各タスクの後にレビュー
- 問題が複合化する前に捕捉
- 次のタスクへ進む前に修正

**Executing Plans:**
- 各バッチ (3 タスク) の後にレビュー
- フィードバックを得て適用し、続行

**アドホック開発:**
- マージ前にレビュー
- 行き詰まったらレビュー

## レッドフラグ

**絶対にしない:**
- 「簡単だから」とレビューを省略
- Critical 問題を無視
- Important 問題を未修正のまま進める
- 正当な技術フィードバックに反論する

**レビュアーが間違っている場合:**
- 技術的理由で押し返す
- 動作を示すコード/テストを提示
- 確認を求める

テンプレート: requesting-code-review/code-reviewer.md
