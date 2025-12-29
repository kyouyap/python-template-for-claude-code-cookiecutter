# スキル作成のベストプラクティス

> Claude が発見し、成功裏に使えるスキルを書く方法を学ぶ。

良いスキルは簡潔で、構造化され、実際の利用でテストされている。このガイドは、Claude が発見し効果的に使えるスキルを書くための実践的な判断基準を提供する。

スキルの概念的な背景は [Skills overview](/en/docs/agents-and-tools/agent-skills/overview) を参照。

## コア原則

### 簡潔さが最重要

[コンテキストウィンドウ](https://platform.claude.com/docs/en/build-with-claude/context-windows)は公共財である。スキルは、Claude が知るべき他のすべてとコンテキストを共有する:

* システムプロンプト
* 会話履歴
* 他スキルのメタデータ
* 実際のリクエスト

スキル内のすべてのトークンが即座にコストになるわけではない。起動時に事前ロードされるのは各スキルのメタデータ（name と description）のみ。Claude はスキルが関連する時だけ SKILL.md を読み、追加ファイルは必要時に読む。しかし SKILL.md を簡潔にすることは依然重要である。いったんロードされると、すべてのトークンが会話履歴や他のコンテキストと競合する。

**デフォルトの前提**: Claude はすでに賢い

Claude がすでに知っていることは書かない。各情報を問い直す:

* "Claude は本当にこの説明が必要か？"
* "Claude が知っていると仮定できるか？"
* "この段落はトークンコストに見合うか？"

**良い例: 簡潔**（約 50 トークン）:

````markdown  theme={null}
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**悪い例: 冗長すぎる**（約 150 トークン）:

```markdown  theme={null}
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

簡潔な版は、PDF が何かやライブラリの扱い方を Claude が知っていると仮定している。

### 適切な自由度を設定する

タスクの脆さや変動性に合わせて具体性を調整する。

**自由度: 高**（テキストベース指示）:

使う場面:

* 複数のアプローチが有効
* 文脈により判断が変わる
* ヒューリスティクスで導く

例:

```markdown  theme={null}
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

**自由度: 中**（疑似コードやパラメータ付きスクリプト）:

使う場面:

* 望ましいパターンがある
* 多少の変化は許容される
* 設定で挙動が変わる

例:

````markdown  theme={null}
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**自由度: 低**（具体スクリプト、パラメータ少）:

使う場面:

* 操作が壊れやすく、エラーが起きやすい
* 一貫性が重要
* 特定の順序が必須

例:

````markdown  theme={null}
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

**たとえ話**: Claude を道を進むロボットと考える:

* **両側が崖の細い橋**: 安全な進路は一つ。低自由度で具体的なガードレールと手順が必要。例: 厳密順序の DB マイグレーション。
* **危険のない広い平原**: 多くの道が成功に至る。高自由度で方針だけ示し、最適経路を任せる。例: 文脈に依存するコードレビュー。

### 使う予定の全モデルでテストする

スキルはモデルへの追加であり、効果は基盤モデルに依存する。使用する全モデルでテストすること。

**モデル別のテスト観点**:

* **Claude Haiku**（高速・低コスト）: スキルが十分なガイダンスを提供しているか？
* **Claude Sonnet**（バランス型）: スキルが明確で効率的か？
* **Claude Opus**（高推論）: 過剰説明を避けているか？

Opus で完璧でも Haiku には詳細が必要なことがある。複数モデルで使うなら、すべてに通用する指示を目指す。

## スキル構造

<Note>
  **YAML フロントマター**: SKILL.md のフロントマターは 2 フィールドのみ:

  * `name` - スキル名（最大 64 文字）
  * `description` - 何をするか + いつ使うかの 1 行説明（最大 1024 文字）

  スキル構造の詳細は [Skills overview](/en/docs/agents-and-tools/agent-skills/overview#skill-structure) を参照。
</Note>

### 命名規則

スキルを参照・議論しやすくするため、一貫した命名パターンを使う。**動名詞（動詞 + -ing）** を推奨する。提供される活動や能力が明確になる。

**良い例（動名詞）**:

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**許容される代替**:

* 名詞句: "PDF Processing", "Spreadsheet Analysis"
* 行動志向: "Process PDFs", "Analyze Spreadsheets"

**避ける**:

* 曖昧: "Helper", "Utils", "Tools"
* 過度に一般的: "Documents", "Data", "Files"
* スキル集合内での不統一

一貫性があると:

* ドキュメントや会話で参照しやすい
* 何をするスキルか一目で分かる
* 複数スキルの整理・検索が容易
* プロフェッショナルで一貫したスキル集になる

### 効果的な description の書き方

`description` はスキル発見に使われ、**何をするか**と**いつ使うか**を含める。

<Warning>
  **必ず三人称で書くこと。** description はシステムプロンプトに挿入され、視点が不一致だと発見に支障が出る。

  * **Good:** "Processes Excel files and generates reports"
  * **Avoid:** "I can help you process Excel files"
  * **Avoid:** "You can use this to process Excel files"
</Warning>

**具体的でキーワードを含める。** 何をするかに加え、いつ使うかの具体的なトリガ/文脈を含める。

スキルは description が 1 つだけ。Claude は 100+ スキルの中から選ぶため、description が選択の鍵になる。description は選択に十分な情報を持ち、SKILL.md 本文が詳細を提供する。

効果的な例:

**PDF Processing スキル:**

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel Analysis スキル:**

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git Commit Helper スキル:**

```yaml  theme={null}
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避けるべき曖昧な description:

```yaml  theme={null}
description: Helps with documents
```

```yaml  theme={null}
description: Processes data
```

```yaml  theme={null}
description: Does stuff with files
```

### プログレッシブ・ディスクロージャ（段階的開示）パターン

SKILL.md は概要として機能し、必要に応じて詳細資料に導く。段階的開示の説明は [How Skills work](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work) を参照。

**実践ガイダンス:**

* SKILL.md 本文は 500 行未満にする
* 上限に近づいたら別ファイルに分割
* 以下のパターンで指示・コード・リソースを整理

#### ビジュアル概要: 単純 → 複雑

基本スキルは SKILL.md のみ:

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="YAML frontmatter と markdown 本文を持つ単一 SKILL.md" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

スキルが成長したら、必要時のみ読まれる追加コンテンツを束ねる:

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="reference.md と forms.md などの追加参照ファイルを束ねる" data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

完全なディレクトリ構成例:

```
pdf/
├── SKILL.md              # メイン指示（トリガ時に読み込まれる）
├── FORMS.md              # フォーム入力ガイド（必要時に読み込まれる）
├── reference.md          # API リファレンス（必要時に読み込まれる）
├── examples.md           # 使用例（必要時に読み込まれる）
└── scripts/
    ├── analyze_form.py   # ユーティリティスクリプト（実行用、読み込まない）
    ├── fill_form.py      # フォーム入力スクリプト
    └── validate.py       # バリデーションスクリプト
```

#### パターン1: 参照付きの高レベルガイド

````markdown  theme={null}
---
name: PDF Processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Claude は必要時に FORMS.md、REFERENCE.md、EXAMPLES.md を読む。

#### パターン2: ドメイン別構成

複数ドメインを持つスキルでは、ドメイン単位で整理し無関係な文脈の読み込みを避ける。売上メトリクスの質問に、財務やマーケのスキーマを読む必要はない。トークンを節約し、文脈を集中させる。

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md theme={null}
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### パターン3: 条件付き詳細

基本を示し、詳細はリンクする:

```markdown  theme={null}
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

必要に応じて REDLINING.md や OOXML.md を読む。

### 深いネスト参照を避ける

Claude は参照先のファイルからさらに参照されるファイルを部分的にしか読まないことがある。`head -100` のようなコマンドでプレビューし、内容が不完全になるリスクがある。

**参照は SKILL.md から 1 段階までにする。** すべての参照ファイルは SKILL.md から直接リンクすることで、必要時に完全に読まれる。

**悪い例: 深すぎる**:

```markdown  theme={null}
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**良い例: 1 段階**:

```markdown  theme={null}
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### 長い参照ファイルには目次を付ける

100 行を超える参照ファイルには冒頭に目次を置く。部分読みでも全体像が見える。

**例**:

```markdown  theme={null}
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

Claude は必要に応じて全文を読むか、特定節へ移動できる。

ファイルシステム 기반 の段階的開示が可能な理由は、後述の [Runtime environment](#runtime-environment) を参照。

## ワークフローとフィードバックループ

### 複雑タスクにはワークフローを使う

複雑な操作は明確な順序ステップに分解する。特に複雑なワークフローでは、Claude がコピーして進捗をチェックできるチェックリストを提供する。

**例1: 研究まとめワークフロー**（コード不要のスキル向け）:

````markdown  theme={null}
## Research synthesis workflow

Copy this checklist and track your progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in the `sources/` directory. Note the main arguments and supporting evidence.

**Step 2: Identify key themes**

Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?

**Step 3: Cross-reference claims**

For each major claim, verify it appears in the source material. Note which source supports each point.

**Step 4: Create structured summary**

Organize findings by theme. Include:
- Main claim
- Supporting evidence from sources
- Conflicting viewpoints (if any)

**Step 5: Verify citations**

Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
````

この例はコード不要の分析タスクにもワークフローが有効なことを示す。チェックリストはどんな複雑な多段プロセスにも使える。

**例2: PDF フォーム入力ワークフロー**（コードありのスキル向け）:

````markdown  theme={null}
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
````

明確なステップは重要な検証をスキップさせない。チェックリストは Claude と人間の進捗管理に有効。

### フィードバックループを実装する

**共通パターン**: バリデータ実行 → エラー修正 → 再実行

このパターンは品質を大きく向上させる。

**例1: スタイルガイド準拠**（コードなし）:

```markdown  theme={null}
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
```

これは参照ドキュメントを検証器として使う例。STYLE_GUIDE.md がバリデータで、Claude が読んで比較する。

**例2: ドキュメント編集プロセス**（コードあり）:

```markdown  theme={null}
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

検証ループが早期にエラーを捕捉する。

## コンテンツガイドライン

### 時間依存情報を避ける

古くなる情報は書かない:

**悪い例: 時間依存**（将来誤りになる）:

```markdown  theme={null}
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**良い例**（"old patterns" セクションを使う）:

```markdown  theme={null}
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

旧パターンで歴史的文脈を残しつつ、本文を汚さない。

### 用語を一貫させる

1つの用語を選び、全体で統一する:

**良い - 一貫性**:

* 常に "API endpoint"
* 常に "field"
* 常に "extract"

**悪い - 不一致**:

* "API endpoint" / "URL" / "API route" / "path" を混在
* "field" / "box" / "element" / "control" を混在
* "extract" / "pull" / "get" / "retrieve" を混在

一貫性があると Claude は指示を理解しやすい。

## 共通パターン

### テンプレートパターン

出力形式のテンプレートを提供する。厳格さは必要度に合わせる。

**厳格な要件向け**（API 応答やデータ形式など）:

````markdown  theme={null}
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**柔軟なガイダンス向け**（調整が有効な場合）:

````markdown  theme={null}
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
````

### 例パターン

出力品質が例に依存するスキルでは、入力/出力ペアを提示する。通常のプロンプトと同じ形式。

````markdown  theme={null}
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
````

例は説明だけよりも、望ましいスタイルと詳細度を明確にする。

### 条件付きワークフローパターン

意思決定点を案内する:

```markdown  theme={null}
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

<Tip>
  ワークフローが大きく複雑な場合は、別ファイルに分けて、タスクに応じて読むよう指示すると良い。
</Tip>

## 評価と反復

### 評価を先に作る

**詳細文書を書く前に評価を作る。** これにより、架空の問題ではなく実際の問題を解決する。

**評価駆動開発:**

1. **ギャップを特定**: スキルなしで代表タスクを実行し、具体的な失敗や欠落を記録
2. **評価を作成**: そのギャップを検証する3つのシナリオを作る
3. **ベースラインを確立**: スキルなしの性能を測定
4. **最小指示を書く**: ギャップを埋め、評価を通す最小限の内容を書く
5. **反復**: 評価を実行し、ベースラインと比較して改善

このアプローチは、実在の問題を解決することを保証する。

**評価構造**:

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  この例はシンプルな評価ルーブリックを持つデータ駆動評価。現状、組み込み評価実行機能はない。ユーザーが独自評価システムを作る。評価がスキル効果測定の唯一の真実となる。
</Note>

### Claude と反復的にスキルを作る

最も効果的なスキル開発は Claude 自身を使うこと。1つの Claude インスタンス（"Claude A"）と協働してスキルを作り、別のインスタンス（"Claude B"）でテストする。Claude は効果的な指示の書き方と必要情報を理解しているため有効。

**新しいスキルを作る:**

1. **スキルなしでタスクを完了**: Claude A と通常プロンプトで問題に取り組む。作業中に文脈・好み・手順知識を自然に提供する。繰り返し提供する情報を意識する。

2. **再利用可能なパターンを特定**: タスク後、類似タスクに役立つ情報を特定。

   **例**: BigQuery 分析なら、テーブル名、フィールド定義、フィルタ規則（"テストアカウントは除外"）、共通クエリパターン。

3. **Claude A にスキル作成を依頼**: "今の BigQuery 分析パターンをスキル化して。テーブルスキーマ、命名規約、テストアカウント除外ルールを含めて。"

   <Tip>
     Claude はスキル形式を理解している。特別なシステムプロンプトや "writing skills" スキルは不要。スキル作成を依頼すれば、適切なフロントマターと本文を持つ SKILL.md を生成する。
   </Tip>

4. **簡潔さをレビュー**: Claude A が不要な説明を追加していないか確認。"勝率の意味説明は削除して、Claude は知っている" など。

5. **情報アーキテクチャ改善**: 例えば "テーブルスキーマは別の参照ファイルに。後でテーブルを追加する可能性がある" と整理を依頼。

6. **類似タスクでテスト**: スキルを読み込んだ新しい Claude B に関連ユースケースを実行させる。正しい情報を見つけ、ルールを適用し、タスクを成功させるか観察。

7. **観察に基づき反復**: Claude B が苦戦/漏れがあれば、Claude A に具体的に伝える。"このスキルで Claude が Q4 の日付フィルタを忘れた。日付フィルタのパターンを追加すべき？"

**既存スキルの反復:**

改善でも同じ階層パターンが続く:

* **Claude A と作業**（改善の専門家）
* **Claude B でテスト**（スキルを使って実作業）
* **Claude B の挙動を観察**し、知見を Claude A に戻す

1. **実ワークフローでスキル使用**: Claude B（スキルあり）に実タスクを与える

2. **Claude B の挙動を観察**: つまづき、成功、予想外の選択を記録

   **例**: "地域別売上レポートを頼んだら、クエリは書いたがテストアカウントの除外を忘れた。スキルには書いてあるのに。"

3. **Claude A に改善依頼**: 現行 SKILL.md と観察を共有。"テストアカウント除外を忘れた。スキルには書いてあるが目立たないのかも？"

4. **Claude A の提案をレビュー**: "MUST filter" のような強い言葉にする、ルールを冒頭に移す、ワークフローを再構成、など。

5. **変更を適用して再テスト**: Claude A の改善を反映し、Claude B で再テスト

6. **利用に基づき反復**: 新しいシナリオで見つかった課題に応じて観察→改善→テストを続ける。各反復は実挙動に基づいてスキルを強化する。

**チームフィードバックの収集:**

1. スキルをチームに共有し、使用を観察
2. スキルは期待通り起動するか？指示は明確か？足りないものは？と質問
3. 自分の盲点を補うためフィードバックを取り込む

**なぜ有効か:** Claude A はエージェントの必要を理解し、あなたはドメイン知識を提供し、Claude B は実利用でギャップを露呈する。観察に基づく反復でスキルが改善される。

### Claude のスキル利用を観察する

反復中は、Claude が実際にスキルをどう使うかに注意する:

* **予想外の探索経路**: 予期しない順番で読むなら構造が直感的でない可能性
* **リンクの見落とし**: 重要ファイルへの参照を辿らないなら、リンクの明示性や目立ち方を改善
* **特定セクションへの過度依存**: 同じファイルばかり読むなら、その内容を SKILL.md に移すべきか検討
* **無視される内容**: バンドルファイルが読まれないなら不要か、導線が弱い

想定ではなく観察で反復する。特にメタデータの 'name' と 'description' は重要。Claude はこれでスキル起動を判断する。何をするか、いつ使うかを明確に記述する。

## 避けるべきアンチパターン

### Windows 形式パスを避ける

Windows でもパスは必ずスラッシュ:

* ✓ **Good**: `scripts/helper.py`, `reference/guide.md`
* ✗ **Avoid**: `scripts\helper.py`, `reference\guide.md`

Unix 形式は全プラットフォームで通用するが、Windows 形式は Unix で失敗する。

### 選択肢を与えすぎない

必要がない限り複数アプローチを並べない:

````markdown  theme={null}
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

## 高度: 実行可能コードを含むスキル

以下は実行スクリプトを含むスキル向け。markdown 指示のみのスキルなら [Checklist for effective Skills](#checklist-for-effective-skills) へ。

### 問題を解決し、丸投げしない

スキル用スクリプトはエラーを Claude に丸投げせず処理する。

**良い例: 明示的なエラーハンドリング**:

```python  theme={null}
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```

**悪い例: Claude に丸投げ**:

```python  theme={null}
def process_file(path):
    # Just fail and let Claude figure it out
    return open(path).read()
```

設定パラメータも正当化と記述が必要。そうしないと "voodoo constants"（Ousterhout の法則）になる。値の根拠がないと Claude が判断できない。

**良い例: 自己説明的**:

```python  theme={null}
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**悪い例: マジックナンバー**:

```python  theme={null}
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### ユーティリティスクリプトを用意する

Claude が書けるとしても、事前に用意したスクリプトには利点がある:

**利点:**

* 生成コードより信頼性が高い
* トークン節約（コードをコンテキストに含めない）
* 時間節約（コード生成不要）
* 利用間で一貫性がある

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="指示ファイルと実行スクリプトの同梱" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

上の図は実行スクリプトと指示ファイルの連携を示す。指示ファイル（forms.md）がスクリプトを参照し、Claude は内容を読み込まずに実行できる。コンテキストを消費するのは出力のみ。

**重要な区別**: 指示で Claude に何をさせるかを明確にする:

* **スクリプトを実行する**（通常）: "Run `analyze_form.py` to extract fields"
* **参照として読む**（複雑ロジックの場合）: "See `analyze_form.py` for the field extraction algorithm"

多くのユーティリティでは実行が望ましい。信頼性が高く効率的。実行の仕組みは [Runtime environment](#runtime-environment) を参照。

**例**:

````markdown  theme={null}
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### 視覚解析を使う

入力を画像化できるなら、Claude に視覚解析させる:

````markdown  theme={null}
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
````

<Note>
  この例では `pdf_to_images.py` を用意する必要がある。
</Note>

Claude の視覚能力はレイアウトや構造の理解に役立つ。

### 検証可能な中間出力を作る

Claude が複雑なオープンエンド作業を行うとき、誤りが起きる。"計画 → 検証 → 実行" パターンで、計画を構造化して作成させ、スクリプトで検証した上で実行することで、早期にミスを防げる。

**例**: PDF の 50 フィールドをスプレッドシートに基づいて更新させる場合。検証がなければ、存在しないフィールド参照、値の競合、必須項目の欠落、誤適用などが起きる。

**解決策**: 上のフォーム入力ワークフローに中間 `changes.json` を追加し、変更適用前に検証する。フローは analyze → **plan file 作成** → **plan を検証** → 実行 → 検証。

**このパターンが効く理由:**

* **早期エラー検出**: 変更前に問題を捕捉
* **機械検証**: スクリプトが客観的に検証
* **可逆の計画**: 原本に触れずに計画を反復できる
* **明確なデバッグ**: エラーメッセージが具体的な問題を指す

**使う場面**: バッチ操作、破壊的変更、複雑な検証規則、重大操作。

**実装のコツ**: 検証スクリプトは "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed" のような具体メッセージにする。Claude が修正しやすい。

### 依存パッケージ

スキルはプラットフォームごとの制限がある実行環境で動く:

* **claude.ai**: npm/PyPI のパッケージをインストール可能、GitHub も取得可能
* **Anthropic API**: ネットワークアクセスなし、実行時インストールなし

SKILL.md に必要パッケージを記載し、[code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool) で利用可能か確認する。

### 実行環境

スキルはファイルシステムアクセス、bash コマンド、コード実行能力を持つ環境で動く。概念説明は [The Skills architecture](/en/docs/agents-and-tools/agent-skills/overview#the-skills-architecture) を参照。

**執筆への影響:**

**Claude のスキルアクセス方法:**

1. **メタデータ事前ロード**: すべてのスキルの YAML frontmatter から name と description がシステムプロンプトにロードされる
2. **必要時にファイルを読む**: bash の Read ツールで SKILL.md などを読む
3. **スクリプトの効率的実行**: スクリプトは内容をコンテキストに入れず実行できる。トークンを消費するのは出力だけ
4. **大きなファイルのコンテキストペナルティなし**: 参照ファイルやデータは読むまでトークンを消費しない

* **パスは重要**: スキルディレクトリはファイルシステムとして辿られる。`reference/guide.md` のようにスラッシュを使う
* **ファイル名を説明的に**: `form_validation_rules.md` のように内容が分かる名前
* **発見しやすく整理**: ドメイン/機能で構成
  * Good: `reference/finance.md`, `reference/sales.md`
  * Bad: `docs/file1.md`, `docs/file2.md`
* **包括的リソースを同梱**: 完全な API docs、大きな例、データセットを入れても読むまでコンテキストコストなし
* **決定的操作はスクリプトに**: `validate_form.py` を書く。Claude に生成させない
* **実行意図を明確に**:
  * "Run `analyze_form.py` to extract fields"（実行）
  * "See `analyze_form.py` for the extraction algorithm"（参照）
* **ファイルアクセスをテスト**: 実リクエストでディレクトリ構成を辿れるか確認

**例:**

```
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

ユーザーが revenue を尋ねたら Claude は SKILL.md を読み、`reference/finance.md` を参照し bash でそのファイルだけ読む。sales.md と product.md は必要になるまで 0 トークン。これが段階的開示の基盤となる。

技術詳細は [How Skills work](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work) を参照。

### MCP ツール参照

MCP（Model Context Protocol）ツールを使うスキルでは、ツール名を完全修飾する。"tool not found" を防ぐ。

**形式**: `ServerName:tool_name`

**例**:

```markdown  theme={null}
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

ここで:

* `BigQuery` と `GitHub` は MCP サーバ名
* `bigquery_schema` と `create_issue` は各サーバのツール名

サーバプレフィックスがないと、複数 MCP サーバがある場合にツールが見つからないことがある。

### ツールがインストール済みと仮定しない

依存を仮定しない:

````markdown  theme={null}
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## 技術メモ

### YAML フロントマター要件

SKILL.md のフロントマターは `name`（最大 64 文字）と `description`（最大 1024 文字）のみ。詳細は [Skills overview](/en/docs/agents-and-tools/agent-skills/overview#skill-structure) を参照。

### トークン予算

SKILL.md 本文は 500 行未満が最適。超えるなら前述の段階的開示パターンで分割する。アーキテクチャ詳細は [Skills overview](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work) を参照。

## 効果的なスキルのチェックリスト

共有前に確認:

### コア品質

* [ ] description が具体的でキーワードを含む
* [ ] description に「何をするか」と「いつ使うか」を含む
* [ ] SKILL.md 本文が 500 行未満
* [ ] 追加詳細は別ファイル（必要なら）
* [ ] 時間依存情報がない（または "old patterns" セクションに隔離）
* [ ] 用語の一貫性がある
* [ ] 例が具体的で抽象ではない
* [ ] ファイル参照が 1 段階
* [ ] 段階的開示が適切
* [ ] ワークフローが明確なステップを持つ

### コードとスクリプト

* [ ] スクリプトが問題を解決し、Claude に丸投げしていない
* [ ] エラーハンドリングが明示的で有用
* [ ] "voodoo constants" がない（全値に根拠）
* [ ] 必要パッケージを記載し、利用可能か確認
* [ ] スクリプトに明確なドキュメントがある
* [ ] Windows 形式パスがない（すべてスラッシュ）
* [ ] 重要操作に検証/検査ステップがある
* [ ] 品質クリティカルなタスクにフィードバックループがある

### テスト

* [ ] 少なくとも 3 つの評価を作成
* [ ] Haiku / Sonnet / Opus でテスト
* [ ] 実使用シナリオでテスト
* [ ] チームフィードバックを取り込む（該当する場合）

## 次のステップ

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="/en/docs/claude-code/skills">
    Create and manage Skills in Claude Code
  </Card>

  <Card title="Use Skills with the API" icon="code" href="/en/api/skills-guide">
    Upload and use Skills programmatically
  </Card>
</CardGroup>
