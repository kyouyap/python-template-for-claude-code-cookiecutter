---
name: finishing-a-development-branch
description: 実装が完了しテストが全て通っていて、作業の統合方法を決める必要があるときに使用する。マージ/PR/クリーンアップの構造化された選択肢を提示して開発完了を導く
---

# 開発ブランチの終了

## 概要

明確な選択肢を提示し、選ばれたワークフローを処理して開発作業の完了を導く。

**中核原則:** テスト確認 → 選択肢提示 → 選択の実行 → クリーンアップ。

**開始時に宣言:** 「finishing-a-development-branch の skill を使ってこの作業を完了します。」

## プロセス

### ステップ 1: テストの確認

**選択肢を提示する前に、テストが通ることを確認する:**

```bash
# プロジェクトのテストスイートを実行
npm test / cargo test / pytest / go test ./...
```

**テストが失敗した場合:**
```
テスト失敗 (<N> 件)。完了前に修正が必要:

[Show failures]

テストが通るまでマージ/PR は進められません。
```

停止する。ステップ 2 に進まない。

**テストが通った場合:** ステップ 2 に進む。

### ステップ 2: ベースブランチの特定

```bash
# 一般的なベースブランチを試す
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

または質問: 「このブランチは main から分岐しました - それで合っていますか?」

### ステップ 3: 選択肢の提示

以下の 4 つの選択肢を正確に提示する:

```
実装は完了しました。どうしますか?

1. <base-branch> にローカルでマージする
2. push して Pull Request を作成する
3. ブランチをそのまま保持する (後で対応)
4. この作業を破棄する

どの選択肢にしますか?
```

**説明は追加しない** - 選択肢は簡潔に保つ。

### ステップ 4: 選択の実行

#### 選択肢 1: ローカルでマージ

```bash
# ベースブランチに切り替え
git checkout <base-branch>

# 最新を取得
git pull

# feature ブランチをマージ
git merge <feature-branch>

# マージ後にテストを確認
<test command>

# テストが通ったら
git branch -d <feature-branch>
```

次に: worktree をクリーンアップ (ステップ 5)

#### 選択肢 2: Push して PR を作成

```bash
# ブランチを push
git push -u origin <feature-branch>

# PR を作成
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

次に: worktree をクリーンアップ (ステップ 5)

#### 選択肢 3: そのまま保持

報告: 「ブランチ <name> を保持します。worktree は <path> に保持します。」

**worktree をクリーンアップしない。**

#### 選択肢 4: 破棄

**まず確認:**
```
次を永久に削除します:
- ブランチ <name>
- 全コミット: <commit-list>
- <path> の worktree

確認のため 'discard' と入力してください。
```

正確な確認を待つ。

確認されたら:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

次に: worktree をクリーンアップ (ステップ 5)

### ステップ 5: worktree のクリーンアップ

**選択肢 1, 2, 4 の場合:**

worktree 内か確認:
```bash
git worktree list | grep $(git branch --show-current)
```

該当する場合:
```bash
git worktree remove <worktree-path>
```

**選択肢 3 の場合:** worktree を保持する。

## クイックリファレンス

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## よくあるミス

**テスト確認の省略**
- **問題:** 壊れたコードをマージし、失敗する PR を作る
- **対策:** 選択肢を提示する前に必ずテストを確認

**自由形式の質問**
- **問題:** 「次にどうすればいい?」→ 曖昧
- **対策:** 構造化された 4 つの選択肢を正確に提示

**自動 worktree クリーンアップ**
- **問題:** 必要かもしれないのに削除する (選択肢 2, 3)
- **対策:** 選択肢 1 と 4 のときだけクリーンアップ

**破棄の確認なし**
- **問題:** 誤って作業を削除する
- **対策:** "discard" の入力確認を必須にする

## レッドフラグ

**絶対にしない:**
- テスト失敗のまま進める
- 結果のテスト確認なしにマージする
- 確認なしに作業を削除する
- 明示的な依頼なしに force-push する

**必ず行う:**
- 選択肢提示前にテストを確認する
- 選択肢は正確に 4 つ提示する
- 選択肢 4 では入力確認を得る
- worktree のクリーンアップは選択肢 1 と 4 のみ

## 連携

**呼び出し元:**
- **subagent-driven-development** (ステップ 7) - 全タスク完了後
- **executing-plans** (ステップ 5) - 全バッチ完了後

**関連 skill:**
- **using-git-worktrees** - その skill が作った worktree をクリーンアップ
