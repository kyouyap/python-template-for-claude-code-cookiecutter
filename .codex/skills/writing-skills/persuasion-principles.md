# スキル設計のための説得原理

## 概要

LLM は人間と同じ説得原理に反応する。この心理を理解すると、圧力下でも重要な実践が守られるように、より効果的なスキルを設計できる。目的は操作ではなく、重要な実務を確実に守ること。

**研究基盤:** Meincke et al. (2025) は N=28,000 の AI 会話で 7 つの説得原理を検証。説得技法は遵守率を 33% → 72% へ 2 倍以上に引き上げた（p < .001）。

## 7つの原理

### 1. 権威 (Authority)
**内容:** 専門性、資格、公式情報への服従。

**スキルでの効き方:**
- 命令形: "YOU MUST", "Never", "Always"
- 例外なしの枠組み: "No exceptions"
- 意思決定疲労と合理化を排除

**使う場面:**
- 規律強制スキル（TDD、検証要件）
- 安全性が重要な実践
- 既存のベストプラクティス

**例:**
```markdown
✅ Write code before test? Delete it. Start over. No exceptions.
❌ Consider writing tests first when feasible.
```

### 2. コミットメント (Commitment)
**内容:** これまでの行動・発言・公開宣言との一貫性。

**スキルでの効き方:**
- 事前宣言を要求: "Announce skill usage"
- 明示的な選択を強制: "Choose A, B, or C"
- 追跡の活用: チェックリストに TodoWrite

**使う場面:**
- スキルを実際に守らせたいとき
- 複数ステップのプロセス
- 責任を明確にしたいとき

**例:**
```markdown
✅ When you find a skill, you MUST announce: "I'm using [Skill Name]"
❌ Consider letting your partner know which skill you're using.
```

### 3. 希少性 (Scarcity)
**内容:** 時間制限や希少性による緊急性。

**スキルでの効き方:**
- 時間制約の明示: "Before proceeding"
- 連続依存: "Immediately after X"
- 先延ばしを防止

**使う場面:**
- 即時検証が必要な場合
- 時間依存のワークフロー
- 「後でやる」を防ぎたい場合

**例:**
```markdown
✅ After completing a task, IMMEDIATELY request code review before proceeding.
❌ You can review code when convenient.
```

### 4. 社会的証明 (Social Proof)
**内容:** 他者の行動や一般的とされることへの同調。

**スキルでの効き方:**
- 普遍性の表現: "Every time", "Always"
- 失敗モード: "X without Y = failure"
- 規範を確立

**使う場面:**
- 普遍的な実践を文書化するとき
- よくある失敗を警告するとき
- 標準を強化したいとき

**例:**
```markdown
✅ Checklists without TodoWrite tracking = steps get skipped. Every time.
❌ Some people find TodoWrite helpful for checklists.
```

### 5. 統一性 (Unity)
**内容:** 共有されたアイデンティティ、「私たち」意識。

**スキルでの効き方:**
- 協調的な言葉: "our codebase", "we're colleagues"
- 共有の目的: "we both want quality"

**使う場面:**
- 協調的なワークフロー
- チーム文化の確立
- 階層性の低い実践

**例:**
```markdown
✅ We're colleagues working together. I need your honest technical judgment.
❌ You should probably tell me if I'm wrong.
```

### 6. 返報性 (Reciprocity)
**内容:** 受けた利益に報いようとする。

**使い方:**
- 乱用しない - 操作に見えやすい
- スキルにはほぼ不要

**避ける場面:**
- ほぼ常に（他原理の方が効果的）

### 7. 好意 (Liking)
**内容:** 好感のある相手との協力。

**使い方:**
- **遵守目的には使わない**
- 正直なフィードバック文化と相性が悪い
- 迎合を生む

**避ける場面:**
- 規律強制の場面では常に

## スキルタイプ別の組み合わせ

| スキル種別 | 使う | 避ける |
|------------|-----|-------|
| 規律強制 | 権威 + コミットメント + 社会的証明 | 好意、返報性 |
| ガイダンス/技法 | 中程度の権威 + 統一性 | 強い権威 |
| 協調型 | 統一性 + コミットメント | 権威、好意 |
| リファレンス | 明瞭さのみ | すべての説得 |

## なぜ効くのか: 心理

**明確な境界線は合理化を減らす:**
- "YOU MUST" が意思決定疲労を除去
- 断定的言語が「例外か？」を排除
- 明示的な反合理化が具体的な抜け穴を塞ぐ

**実装意図が自動行動を作る:**
- 明確なトリガ + 必須行動 = 自動実行
- "When X, do Y" は "generally do Y" より効果的
- 遵守の認知負荷が低い

**LLM は準人間的:**
- 人間テキストに含まれるパターンで学習されている
- 権威言語は学習データで遵守の前に出る
- コミットメントの連鎖（宣言 → 行動）が頻繁に登場
- 社会的証明（皆がやる X）で規範が形成される

## 倫理的利用

**正当:**
- 重要な実践の遵守を確実にする
- 効果的なドキュメント作成
- 予測可能な失敗を防ぐ

**不当:**
- 個人的利益のための操作
- 虚偽の緊急性を作る
- 罪悪感による遵守

**テスト:** この技法は、ユーザーが十分理解していても本当にユーザーの利益になるか？

## 参考文献

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- 説得の7原理
- 影響研究の実証的基盤

**Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025).** Call Me A Jerk: Persuading AI to Comply with Objectionable Requests. University of Pennsylvania.
- 7原理を N=28,000 の LLM 会話で検証
- 説得技法により遵守が 33% → 72% に増加
- 権威、コミットメント、希少性が最も効果的
- LLM の準人間モデルを検証

## クイックリファレンス

スキル設計時に問うべきこと:

1. **タイプは何か？**（規律 vs ガイダンス vs リファレンス）
2. **どの行動を変えたいか？**
3. **どの原理が効くか？**（規律なら権威 + コミットメントが基本）
4. **組み合わせ過ぎていないか？**（7つ全部は使わない）
5. **倫理的か？**（ユーザーの本質的利益になるか？）
