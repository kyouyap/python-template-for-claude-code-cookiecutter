# コード品質レビュアー用プロンプトテンプレート

コード品質レビュアーのサブエージェントをディスパッチするときにこのテンプレートを使用する。

**目的:** 実装がよくできているかを検証する (クリーン、テスト済み、保守性)

**仕様適合レビューが通過した後にのみディスパッチする。**

```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

**コードレビュアーの返答:** Strengths、Issues (Critical/Important/Minor)、Assessment
