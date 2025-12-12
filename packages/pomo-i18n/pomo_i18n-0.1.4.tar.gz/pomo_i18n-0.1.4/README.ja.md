# pomo-i18n

[English](README.md) | **日本語**

![Tests](https://github.com/kimikato/pomo-i18n/actions/workflows/tests.yml/badge.svg?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/pomo-i18n.svg)](https://pypi.org/project/pomo-i18n/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

`pomo-i18n` は Python 向けのシンプルで厳密型付け（strict typing）な gettext 互換の国際化ライブラリです。

`.po` と `.mo` ファイルを自前でパースし、外部依存なしで `gettext()` / `ngettext()` を使用できるようにします。

---

## 特長

- ✔ `.po` ファイル、 `.mo` ファイルをパース（ gettext 形式）
- ✔ 複数形ルール（`Plural-Forms:`） を解析し、複雑な複数形ルールに対応
- ✔ mypy / Pylance 完全対応（ strict モード）
- ✔ gettext 互換 API `gettext` / `ngettext` / `translation`
- ✔ OS 依存なし（libintl 不要）
- ✔ Linux / macOS / Windows で動作

CLI ツールや API サーバ、バッチ処理など
Python プロジェクトへの組み込みを想定しています。

---

## インストール

```sh
pip install pomo-i18n
```

もしくは `src/` 内に同梱して使用することもできます。

```
src/
 └─ pypomo/
```

---

## ドキュメント

より詳細な技術仕様（API リファレンス / ベンチマーク結果）は英語版ドキュメントをご覧ください。

- [API リファレンス](docs/api.md) （英語版）
- [ベンチマーク結果](docs/benchmarks.md) （英語版）

---

## クイックスタート

```python
from pypomo.gettext import translation

t = translation(
    domain="messages",
    localedir="locales",
    languages=["ja"],
)

_ = t.gettext

print(_("Hello"))                     # -> 「こんにちは」等
print(t.ngettext("apple", "apples", 1))   # -> 「りんご」
print(t.ngettext("apple", "apples", 3))   # -> 「りんご」(日本語は単数のみ)
```

フォルダ構成例：

```
locales/
 └─ ja/
     └─ LC_MESSAGES/
         └─ messages.po
```

---

## `.po` の解析

`pomo-i18n` の POParser は、 gettext の基本要素をサポートします：

- `msgid` / `msgstr`
- 複数形：`msgid_plural` / `msgstr[n]`
- 複数行文字列
- gettext のコメント形式に対応：
  - `#`（翻訳者コメント）
  - `#.`（抽出コメント）
  - `#:`（参照コメント）
  - `#, flags`（通常コメントとして処理。`fuzzy` の特別扱いは未対応）
- ヘッダー（`msgid ""`）の解析 -> ここから 複数形ルール（`Plural-Forms:`）を抽出

---

## 複数形ルール（Plural Forms）

`.po` には次のような行が含まれます：

```python
Plural-Forms: nplurals=2; plural=(n != 1);
```

ロシア語の例：

```python
Plural-Forms: nplurals=3;
 plural=(n%10==1 && n%100!=11 ? 0 :
        n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
```

`pomo-i18n` は C 風構文（ `&&` / `||` / `? :` ）を Python 構文に変換し、制限付き `eval()` で安全に評価します。

---

## API リファレンス

### Catalog

```python
from pypomo.catalog import Catalog
```

| メソッド                        | 説明                      |
| ------------------------------- | ------------------------- |
| `gettext(msgid)`                | 単純翻訳                  |
| `ngettext(singular, plural, n)` | 複数形に対応した翻訳      |
| `merge(other)`                  | 他の Catalog をマージする |
| `header_msgstr()`               | ヘッダーを返す            |

---

### トップレベル API

```python
from pypomo.gettext import gettext, ngettext, translation
```

| 関数                                        | 説明                                                 |
| ------------------------------------------- | ---------------------------------------------------- |
| `gettext(msgid)`                            | デフォルトカタログでの翻訳                           |
| `ngettext(singular, plural, n)`             | 複数形を考慮した翻訳                                 |
| `translation(domain, localedir, languages)` | 特定の `.po` ファイルを読み込んで新規 Catalog を返す |

---

## `.mo` ファイルの書き出し

`pomo-i18n` には GNU gettext 互換の `.mo` バイナリを書き出すための `write_mo()` 関数が含まれています。
`Catalog` インスタンスを `.mo` ファイルに変換できます。

### 例： Catalog を `.mo` ファイルとして出力する

```python
from pypomo.catalog import Catalog
from pypomo.mo.writer import write_mo
from pypomo.parser.types import POEntry

entries = [
    POEntry(
        msgid="",
        msgstr=(
            "Language: ja\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Plural-Forms: nplurals=1; plural=0;\n"
        ),
        msgid_plural=None,
        msgstr_plural={},
        comments=[],
    ),
    POEntry(
        msgid="Hello",
        msgstr="こんにちは",
        msgid_plural=None,
        msgstr_plural={},
        comments=[],
    ),
]

catalog = Catalog.from_po_entries(entries)
write_mo("messages.mo", catalog)
```

### 出力した `.mo` の利用方法

Python の標準 `gettext` でロードできます：

```python
import gettext

with open("messages.mo", "rb") as f:
    trans = gettext.GNUTranslations(f)

print(trans.gettext("Hello"))  # -> 「こんにちは」
```

### 特長

- GNU gettext の `.mo` フォーマットと互換
- `msgid=""` がない場合でも自動でヘッダーを生成
- 複数形（nplurals / 複数形判定式）に対応
- 出力は UTF-8、追加依存なし

---

## `.mo` ファイルの読み込み

`pomo-i18n` には GNU gettext 互換の `.mo` バイナリファイルを `Catalog` に読み込むためのローダーが付属しています。

### 例： `.mo` ファイルを `Catalog` として読み込む

```python
from pypomo.mo.loader import load_mo

cat = load_mo("messages.mo")

_ = cat.gettext

print(_("Hello"))       # -> 「こんにちは」など
print(cat.ngettext("apple", "apples", 3))
```

### 対応している内容

- GNU gettext `.mo` バイナリ形式と互換
- リトルエンディアンのマジックナンバー ( 0x9504120E ) を検証
- `msgid ""` からヘッダー情報（`Plural-Forms:` など）を解析
- 複数形ルール（Plural expression）の適切な処理
- 以下のすべてを正しく読み込めます：
  - 単数メッセージ
  - 複数メッセージ（ `msgid "\x00"` で区切る）
  - 複数形の各フォーム（ `msgstr[n]` 相当）

### 動作の流れ

`.mo` ローダーは次のように動作します：

1. `read_mo_binary()`

   バイナリヘッダーと文字列テーブルを読み取り、生の `msgid` / `msgstr` のバイト列を抽出します。

2. `decode_map_pairs()`

   バイト列を Python の構造へ変換します：

   - `"single"`（単数）
   - `"plural-header"`（複数形）

3. `build_catalog_from_pairs()`

   ペアから完全な `Catalog` を構築し、必要に応じて `Plural-Forms:` も設定します。

### `.mo` を使うべきタイミング

`.mo` バイナリを使う利点は以下です：

- `.po` より 読み込みが高速（バイナリのため）
- 本番環境へのデプロイで安定性が高い
- `gettext` や `msgfmt` が生成した `.mo` と完全互換

### `.po` でも `.mo` でも目的に応じて選択が可能

- 編集しやすい： `.po`
- 配布や読み込みが速い： `.mo`

どちらも `pomo-i18n` は自然に扱えるので、目的に応じて `.po` / `.mo` を使い分けられます。

---

## ベンチマーク

2 種類のベンチマークがあります:

### 1. Micro benchmark ( timeit )

```bash
make bench
```

### 2. pytest-benchmark

```bash
make bench-pytest
```

### 🏎 複数形評価 （ Plural Expression ） ベンチマーク

複数形選択（ plural rule evaluation ）は gettext の内部処理で最も頻繁に実行されるため、
キャッシュ方式によりパフォーマンスが大きく変わります。
以下は実際のベンチマーク結果です。

#### 計測環境

- Python 3.10.19
- macOS Tahoe 26.1 (Apple Silicon, M4)
- pytest-benchmark 5.2.3
- pypomo default settings

#### キャッシュ方式ごとの比較結果

| Backend  | Simple Rule ( µs ) | Complex Rule ( µs ) | コメント                               |
| -------- | ------------------ | ------------------- | -------------------------------------- |
| **none** | 約 2.54            | 約 4.83             | キャッシュなし。デバッグ向け。         |
| **weak** | 約 2.69            | 約 4.89             | Python の dict による簡易キャッシュ。  |
| **lru**  | 約 2.49            | 約 4.92             | もっとも高速（ CPython の LRU 実装）。 |

#### まとめ

- 本番利用では **`LRU` キャッシュを推奨**
- `weak` は軽量キャッシュとして扱いやすい
- `none` は比較実験やデバッグ用途に最適

#### キャッシュ方式の切り替え方法

環境変数でキャッシュ backend を切り替えできます：

```bash
# キャッシュ無効化（デバッグ向け）
export PYPOMO_CACHE=none

# dict ベースの簡易キャッシュ
export PYPOMO_CACHE=weak

# LRU キャッシュ（推奨）
export PYPOMO_CACHE=lru

# LRU サイズ変更（デフォルト: 256）
export PYPOMO_PLURAL_CACHE_SIZE=512
```

プログラム中で切り替えることも可能です：

```python
from pypomo.utils.cache_manager import get_default_cache
cache = get_default_cache(backend="lru")
```

---

## 今後の予定

- 複数言語のフォールバック対応
- コメント（ `#, fuzzy`、`#.` など）の強化
- `.pot` の自動生成ツール
- CLI ツールの提供

---

## ライセンス

MIT License
© 2025 Kiminori Kato

---
