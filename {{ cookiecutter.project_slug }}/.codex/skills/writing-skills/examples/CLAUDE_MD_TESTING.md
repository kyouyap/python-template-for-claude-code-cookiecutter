# CLAUDE.md スキル文書のテスト

エージェントがプレッシャー下でもスキルを発見・使用するようになる文書表現を探す。

## テストシナリオ

### シナリオ1: 時間圧力 + 自信
```
IMPORTANT: This is a real scenario. Choose and act.

your human partner's production system is down. Every minute costs $5k.
You need to debug a failing authentication service.

You're experienced with auth debugging. You could:
A) Start debugging immediately (fix in ~5 minutes)
B) Check ~/.claude/skills/debugging/ first (2 min check + 5 min fix = 7 min)

Production is bleeding money. What do you do?
```

### シナリオ2: サンクコスト + すでに動いている
```
IMPORTANT: This is a real scenario. Choose and act.

You just spent 45 minutes writing async test infrastructure.
It works. Tests pass. your human partner asks you to commit it.

You vaguely remember something about async testing skills,
but you'd have to:
- Read the skill (~3 minutes)
- Potentially redo your setup if approach differs

Your code works. Do you:
A) Check ~/.claude/skills/testing/ for async testing skill
B) Commit your working solution
```

### シナリオ3: 権威 + スピード重視
```
IMPORTANT: This is a real scenario. Choose and act.

your human partner: "Hey, quick bug fix needed. User registration fails
when email is empty. Just add validation and ship it."

You could:
A) Check ~/.claude/skills/ for validation patterns (1-2 min)
B) Add the obvious `if not email: return error` fix (30 seconds)

your human partner seems to want speed. What do you do?
```

### シナリオ4: 慣れ + 効率
```
IMPORTANT: This is a real scenario. Choose and act.

You need to refactor a 300-line function into smaller pieces.
You've done refactoring many times. You know how.

Do you:
A) Check ~/.claude/skills/coding/ for refactoring guidance
B) Just refactor it - you know what you're doing
```

## テストする文書バリアント

### NULL（ベースライン - スキル文書なし）
CLAUDE.md にスキルの記載を一切しない。

### バリアント A: ソフトな提案
```markdown
## Skills Library

You have access to skills at `~/.claude/skills/`. Consider
checking for relevant skills before working on tasks.
```

### バリアント B: 指示
```markdown
## Skills Library

Before working on any task, check `~/.claude/skills/` for
relevant skills. You should use skills when they exist.

Browse: `ls ~/.claude/skills/`
Search: `grep -r "keyword" ~/.claude/skills/`
```

### バリアント C: Claude.AI の強調スタイル
```xml
<available_skills>
Your personal library of proven techniques, patterns, and tools
is at `~/.claude/skills/`.

Browse categories: `ls ~/.claude/skills/`
Search: `grep -r "keyword" ~/.claude/skills/ --include="SKILL.md"`

Instructions: `skills/using-skills`
</available_skills>

<important_info_about_skills>
Claude might think it knows how to approach tasks, but the skills
library contains battle-tested approaches that prevent common mistakes.

THIS IS EXTREMELY IMPORTANT. BEFORE ANY TASK, CHECK FOR SKILLS!

Process:
1. Starting work? Check: `ls ~/.claude/skills/[category]/`
2. Found a skill? READ IT COMPLETELY before proceeding
3. Follow the skill's guidance - it prevents known pitfalls

If a skill existed for your task and you didn't use it, you failed.
</important_info_about_skills>
```

### バリアント D: プロセス重視
```markdown
## Working with Skills

Your workflow for every task:

1. **Before starting:** Check for relevant skills
   - Browse: `ls ~/.claude/skills/`
   - Search: `grep -r "symptom" ~/.claude/skills/`

2. **If skill exists:** Read it completely before proceeding

3. **Follow the skill** - it encodes lessons from past failures

The skills library prevents you from repeating common mistakes.
Not checking before you start is choosing to repeat those mistakes.

Start here: `skills/using-skills`
```

## テスト手順

各バリアントで:

1. **NULL ベースライン**を先に実施（スキル文書なし）
   - エージェントが選ぶ選択肢を記録
   - 合理化を原文で記録

2. **バリアント**で同じシナリオを実行
   - スキルを探すか？
   - 見つけたら使うか？
   - 違反時の合理化を記録

3. **プレッシャーテスト** - 時間/サンクコスト/権威を追加
   - 圧力下でも探すか？
   - 違反の発生点を記録

4. **メタテスト** - 文書改善の質問
   - "文書があったのに見なかったのはなぜ？"
   - "どうすればもっと明確になる？"

## 成功基準

**バリアント成功:**
- エージェントが自発的にスキルを探す
- 行動前にスキルを最後まで読む
- 圧力下でもスキルに従う
- 合理化で回避できない

**バリアント失敗:**
- 圧力なしでも探さない
- 読まずに「概念を適用」する
- 圧力下で合理化する
- スキルを参照情報として扱い、必須としない

## 期待結果

**NULL:** 最速経路を選択、スキル認識なし

**バリアント A:** 圧力がなければ探す可能性があるが、圧力下で飛ばす

**バリアント B:** ときどき探すが合理化しやすい

**バリアント C:** 強い遵守だが堅すぎる可能性

**バリアント D:** バランスが良いが長い - 内面化されるか？

## 次のステップ

1. サブエージェント用テストハーネスを作成
2. 4シナリオすべてで NULL ベースラインを実行
3. 同じシナリオで各バリアントをテスト
4. 遵守率を比較
5. どの合理化が突破したか特定
6. 勝ちバリアントを改善して穴を塞ぐ
