---
name: verification-before-completion
description: 作業が完了/修正済み/通過済みと主張する直前、コミットや PR 作成前に使用する。成功の主張をする前に検証コマンドを実行し出力を確認することを要求する。常に主張より証拠
---

# 完了前の検証

## 概要

検証なしに作業完了を主張するのは効率ではなく不誠実。

**中核原則:** いつでも、主張より証拠。

**このルールの文言を破ることは、精神を破ることと同義。**

## 鉄則

```
新しい検証証拠なしに完了を主張しない
```

このメッセージ内で検証コマンドを実行していないなら、通過したと主張できない。

## ゲート関数

```
ステータスを主張したり満足を表明する前に:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## よくある失敗

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## レッドフラグ - 停止

- "should"、"probably"、"seems to" を使う
- 検証前に満足を表明する ("Great!", "Perfect!", "Done!" など)
- 検証なしでコミット/プッシュ/PR をしようとする
- エージェントの成功報告を信用する
- 部分的な検証に頼る
- 「今回だけ」と考える
- 疲れていて早く終わらせたい
- **検証を実行していないのに成功を示唆する表現はすべて**

## 正当化の防止

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## 重要パターン

**テスト:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**回帰テスト (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**ビルド:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**要件:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**エージェント委任:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## なぜ重要か

24 件の失敗記録より:
- 人間パートナーが「信じられない」と言った - 信頼喪失
- 未定義関数が出荷された - クラッシュする
- 要件欠落が出荷された - 不完全な機能
- 誤った完了宣言で時間が無駄 → 方向転換 → 手戻り
- 「誠実さは核の価値。嘘をつけば交代だ」に違反

## 適用タイミング

**必ず先に:**
- 成功/完了のあらゆる主張
- あらゆる満足表現
- 作業状態に関するあらゆる肯定的発言
- コミット、PR 作成、タスク完了
- 次のタスクへ移る前
- エージェントへの委任

**ルールの適用対象:**
- 原文の表現
- 言い換えや同義語
- 成功を示唆する含意
- 完了/正しさを示すあらゆる表現

## 結論

**検証に近道はない。**

コマンドを実行し、出力を読み、それから結果を主張する。

これは譲れない。
