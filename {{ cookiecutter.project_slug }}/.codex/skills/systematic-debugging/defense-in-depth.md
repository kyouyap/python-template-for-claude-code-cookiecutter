# 多層防御バリデーション

## 概要

不正データが原因のバグを直したとき、1箇所の検証で十分に感じる。しかし単一のチェックは、別経路、リファクタリング、モックによって簡単にすり抜ける。

**中核原則:** データが通過するすべての層で検証する。バグを構造的に不可能にする。

## なぜ多層なのか

単一の検証: 「バグを直した」
多層の検証: 「バグを不可能にした」

層ごとに捕捉できるケースが違う:
- 入口の検証は大半のバグを止める
- ビジネスロジックは境界ケースを捉える
- 環境ガードは文脈特有の危険を防ぐ
- デバッグログは他層が抜けたときの手掛かりになる

## 4つの層

### Layer 1: 入口の検証
**目的:** API 境界で明らかに不正な入力を拒否する

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Layer 2: ビジネスロジックの検証
**目的:** この操作に対してデータが意味を持つか確認する

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### Layer 3: 環境ガード
**目的:** 特定の文脈での危険な操作を防ぐ

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `Refusing git init outside temp dir during tests: ${directory}`
      );
    }
  }
  // ... proceed
}
```

### Layer 4: デバッグ計測
**目的:** フォレンジックのために文脈を記録する

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... proceed
}
```

## パターンの適用

バグを見つけたら:

1. **データフローを追跡する** - 不正な値はどこで生まれ、どこで使われるか
2. **すべてのチェックポイントを列挙する** - データが通過するすべての地点を列挙
3. **各層に検証を追加する** - 入口、ビジネス、環境、デバッグ
4. **各層をテストする** - Layer 1 を回避し、Layer 2 が捕捉するか確認

## セッションでの例

バグ: 空の `projectDir` が原因で `git init` がソースコード内で実行された

**データフロー:**
1. テストセットアップ → 空文字
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` が `process.cwd()` で実行される

**追加した4層:**
- Layer 1: `Project.create()` が空/存在/書き込み可を検証
- Layer 2: `WorkspaceManager` が projectDir 空を拒否
- Layer 3: `WorktreeManager` がテスト時の tmpdir 外 git init を拒否
- Layer 4: git init 前のスタックトレースログ

**結果:** 1847 テストが通過、再現不能

## 重要な洞察

4層すべてが必要だった。テスト中、各層が他層の取りこぼしを補った:
- 別経路が入口検証を回避した
- モックがビジネスロジックのチェックを回避した
- 異なるプラットフォームの境界ケースには環境ガードが必要だった
- デバッグログが構造的な誤用を特定した

**1箇所で止めない。** すべての層にチェックを入れる。
