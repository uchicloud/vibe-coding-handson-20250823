# Overview
TDDの実践とその効果の体験のため、与えられた課題を注意深く分析しTDDワークフローに従って解く。

# Specification
- 言語はPythonで開発し、`uv run --with <xxx> --with <yyy>... foo.py`コマンドでポータブルに実行できるようにする。
- `pytest`を利用する。
- テスト(失敗) → 実装 → テスト(成功) のイテレーションを続ける。
- DRY原則に従い、コードを何度も書き直して可読性を向上させる。
- 境界値テスト、例外ケースのテストを盛り込む。

# Task
1. FizzBuzzの実装
2. pygameでpongを実装