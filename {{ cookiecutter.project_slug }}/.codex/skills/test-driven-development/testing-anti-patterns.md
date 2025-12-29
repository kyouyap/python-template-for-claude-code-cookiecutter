# テストのアンチパターン

**このリファレンスを読む場面:** テストを書いたり変更したりするとき、モックを追加するとき、本番コードにテスト専用メソッドを入れたくなったとき。

## 概要

テストは実挙動を検証しなければならない。モックの挙動を検証してはいけない。モックは分離のための手段であり、テスト対象ではない。

**中核原則:** コードの挙動をテストせよ。モックの挙動をテストするな。

**厳密な TDD がこれらのアンチパターンを防ぐ。**

## 鉄則

```
1. モックの挙動をテストしない
2. 本番クラスにテスト専用メソッドを追加しない
3. 依存関係を理解せずにモックしない
```

## アンチパターン1: モックの挙動をテストする

**違反例:**
```typescript
// ❌ BAD: モックの存在をテストしている
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**なぜダメか:**
- モックが動いていることを確認しているだけで、コンポーネントは検証していない
- モックがあると通り、ないと落ちる
- 実挙動について何も分からない

**人間パートナーの指摘:** 「モックの挙動をテストしてない？」

**修正:**
```typescript
// ✅ GOOD: 実コンポーネントをテストするか、モックしない
test('renders sidebar', () => {
  render(<Page />);  // サイドバーはモックしない
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// または、分離のためにサイドバーをモックする必要がある場合:
// モックのアサーションはしない。Page がサイドバー存在時にどう振る舞うかをテストする
```

### ゲート関数

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

## アンチパターン2: 本番コードにテスト専用メソッド

**違反例:**
```typescript
// ❌ BAD: destroy() はテストでしか使わない
class Session {
  async destroy() {  // 本番 API に見える!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// In tests
afterEach(() => session.destroy());
```

**なぜダメか:**
- 本番クラスにテスト専用コードが混入する
- 誤って本番で呼ばれると危険
- YAGNI と責務分離に反する
- オブジェクトのライフサイクルとエンティティのライフサイクルを混同する

**修正:**
```typescript
// ✅ GOOD: テストユーティリティで片付ける
// Session は本番では stateless。destroy() は持たない

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

### ゲート関数

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## アンチパターン3: 依存関係を理解せずにモックする

**違反例:**
```typescript
// ❌ BAD: モックがテストロジックを壊している
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**なぜダメか:**
- モックしたメソッドにテストが依存している副作用（設定書き込み）があった
- 「安全のため」の過剰モックが実挙動を壊す
- 誤った理由で通る/謎の失敗になる

**修正:**
```typescript
// ✅ GOOD: 正しいレベルでモックする
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### ゲート関数

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## アンチパターン4: 不完全なモック

**違反例:**
```typescript
// ❌ BAD: 必要だと思う項目だけを部分的にモック
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};

// Later: breaks when code accesses response.metadata.requestId
```

**なぜダメか:**
- **部分モックは構造的な前提を隠す** - 知っている項目しかモックしない
- **下流コードが含まれていない項目に依存している可能性** - サイレント失敗
- **テストは通るが統合で壊れる** - モックは不完全、実 API は完全
- **偽の安心感** - 実挙動について何も証明しない

**鉄則:** 実際のデータ構造を完全にモックする。テストで使う項目だけではない。

**修正:**
```typescript
// ✅ GOOD: 実 API の完全性を反映
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

### ゲート関数

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## アンチパターン5: 統合テストは後回し

**違反例:**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**なぜダメか:**
- テストは実装の一部であり、任意の後工程ではない
- TDD ならここで防げた
- テストなしで完了とは言えない

**修正:**
```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## モックが複雑すぎるとき

**警告サイン:**
- モック準備がテスト本体より長い
- テストを通すために全部モックしている
- 実コンポーネントが持つメソッドがモックにない
- モックを変えるとテストが壊れる

**人間パートナーの問い:** 「ここでモックが必要？」

**検討:** 実コンポーネントの統合テストの方が、複雑なモックより単純なことが多い

## TDD がこれらのアンチパターンを防ぐ

**TDD が効く理由:**
1. **テスト先行** → 何をテストしているかを自分に強制する
2. **失敗を確認** → モックではなく実挙動をテストしていることを確認する
3. **最小実装** → テスト専用メソッドの混入を防ぐ
4. **実依存** → モック前にテストが実際に何を必要とするか分かる

**モック挙動をテストしていたら TDD を破っている** - 実コードに対して失敗を確認する前にモックを足している。

## クイックリファレンス

| アンチパターン | 修正 |
|--------------|-----|
| モック要素へのアサーション | 実コンポーネントをテストするか、モックを外す |
| 本番にテスト専用メソッド | テストユーティリティへ移動 |
| 理解なしのモック | 依存関係を理解してから最小限でモック |
| 不完全なモック | 実 API を完全に再現 |
| テスト後回し | TDD - テスト先行 |
| 過剰なモック | 統合テストを検討 |

## レッドフラグ

- `*-mock` のテストIDにアサーションしている
- テストファイルでしか呼ばれないメソッドがある
- モック準備がテストの50%以上
- モックを外すとテストが失敗する
- なぜモックが必要か説明できない
- 「安全のため」にモックしている

## 結論

**モックは分離のための道具であり、テスト対象ではない。**

TDD でモック挙動をテストしていると判明したら、やり方を誤っている。

修正: 実挙動をテストするか、そもそもモックが必要かを問い直す。
